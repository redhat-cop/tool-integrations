import gitlab
import yaml
from kubernetes import client, config
from jinja2 import Template
import os

gitlab_api_url = os.environ["GITLAB_API_URL"]
gitlab_token = os.environ["GITLAB_PERSONAL_ACCESS_TOKEN"]
gitlab_group = os.environ["RESIDENCIES_PARENT_REPOSITORIES_ID"]

argo_namespace = os.environ["ARGO_NAMESPACE"]
argo_configmap_name = os.environ["ARGO_CONFIGMAP_NAME"]
destination_namespace = os.environ["DESTINATION_NAMESPACE"]
resource_prefix = os.environ["RESOURCE_PREFIX"]
ssh_secret_name = os.environ["SSH_SECRET_NAME"]
chart_path = os.environ["CHART_PATH"]

if "PROCESS_REPOSITORY_CONDITION" in os.environ:
    use_process_repository_condition = True
    process_repository_condition = os.environ["PROCESS_REPOSITORY_CONDITION"]
else:
    use_process_repository_condition = False
    process_repository_condition = ""

application_template = Template("""apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: "{{ RESOURCE_PREFIX }}-{{ RESOURCE_ID }}"
  labels:
    created-by: gitlab-argo-bridge
spec:
  destination:
    namespace: "{{ DESTINATION_NAMESPACE }}"
    server: 'https://kubernetes.default.svc'
  source:
    path: "{{ CHART_PATH }}"
    repoURL: >-
      {{ REPO_URL }}
    targetRevision: HEAD
  project: default""")

repository_config_template = Template("""- name: {{ RESOURCE_PREFIX }}-{{ RESOURCE_ID }}
  sshPrivateKeySecret:
    key: sshPrivateKey
    name: {{ SSH_SECRET_NAME }}
  type: git
  url: {{ REPO_URL }}
""")

config.load_incluster_config()
custom_object_api = client.CustomObjectsApi()
config_map_api = client.CoreV1Api()


def main() -> None:
    g = gitlab.Gitlab(gitlab_api_url, private_token=gitlab_token)

    current_applications_list = custom_object_api.list_namespaced_custom_object(
        group="argoproj.io",
        version="v1alpha1",
        namespace=argo_namespace,
        plural="applications",
    )
    current_application_names = list(map(lambda item: item["metadata"]["name"], current_applications_list["items"]))

    g.auth()
    group = g.groups.get(gitlab_group)
    for group_project in group.projects.list(all=True, include_subgroups=True):
        project = g.projects.get(group_project.id, lazy=False)
        process_project(project, current_application_names)


def process_project(project, current_application_names) -> None:
    application = application_template.render(
        RESOURCE_ID=project.id,
        RESOURCE_PREFIX=resource_prefix,
        CHART_PATH=chart_path,
        REPO_URL=project.ssh_url_to_repo,
        DESTINATION_NAMESPACE=destination_namespace,
    )
    application_data = yaml.load(application, Loader=yaml.FullLoader)

    # Check if we need to process this one
    print(f"Checking if {application_data['metadata']['name']} should be processed")
    if not application_data["metadata"]["name"] in current_application_names:
        if use_process_repository_condition:
            try:
                # These functions are accessible within the scope of `PROCESS_REPOSITORY_CONDITION`

                def exists(filename, branch="master"):
                    try:
                        project.files.get(file_path=filename, ref=branch)
                        return True
                    except:
                        return False

                def contains(filename, string, branch="master"):
                    try:
                        file = project.files.get(file_path=filename, ref=branch)
                        return string in str(file.decode())
                    except:
                        return False

                scope = locals()
                should_process = eval(process_repository_condition, scope)

            except:
                print(f"Condition check for {application_data['metadata']['name']} resulted in an error (might be expected)")
                should_process = False
        else:
            should_process = True

        if should_process:
            print(f"Adding {application_data['metadata']['name']}")
            add_application_to_argo(project, application_data)
        else:
            print(f"Not processing {application_data['metadata']['name']} because the condition check did not pass")
    else:
        print(f"Will not process {application_data['metadata']['name']} because it already exists")


def add_application_to_argo(project, application_data) -> None:
    # Create Application object in OpenShift
    custom_object_api.create_namespaced_custom_object(
        group="argoproj.io",
        version="v1alpha1",
        namespace=argo_namespace,
        plural="applications",
        body=application_data,
    )

    # Edit ConfigMap to link the repo to an SSH secret
    config_map = config_map_api.read_namespaced_config_map(
        name=argo_configmap_name,
        namespace=argo_namespace,
    )
    repository_config = repository_config_template.render(
        RESOURCE_ID=project.id,
        RESOURCE_PREFIX=resource_prefix,
        REPO_URL=project.ssh_url_to_repo,
        SSH_SECRET_NAME=ssh_secret_name,
    )
    if "repositories" in config_map.data.keys():
        config_map.data['repositories'] += "\n" + repository_config
    else:
        config_map.data['repositories'] = repository_config
    config_map_api.patch_namespaced_config_map(
        name=argo_configmap_name,
        namespace=argo_namespace,
        body=config_map,
    )


main()
