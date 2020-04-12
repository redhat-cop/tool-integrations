# Argo CD GitLab Bridge

This repository provides a method to sync private GitLab repositories in a specific GitLab group with an Argo CD instance.

When deployed, this repo builds an image using Python s2i, and sets up a CronJob which scans GitLab periodically. When it detects a new repository, it adds an Application instance to Argo CD, as well as configures Argo to use a certain SSH secret to pull that repository.

It is deployable using Helm 3, and all options can be seen in the chart's [values file](helm/values.yaml).

## Conditional Processing

The app supports an optional parameter `processRepositoryCondition` (environment variable `PROCESS_REPOSITORY_CONDITION`), which, when populated, runs an additional check against each repo that must pass before it will be added to Argo CD. This parameter is expected to be a valid Python expression, and the following two special functions returning boolean values are available to it:

* `exists(filename, branch="master")`
* `contains(filename, string, branch="master")`

Some example values for `processRepositoryCondition` are:

| Value  | Description  |
|---|---|
| `exists('deploy.yaml')`  | Only process the repository if `deploy.yaml` exists in the root of the project  |
| `exists('helm/values.yaml') and contains('helm/values.yaml', 'deploy: true')`  | Only process the repository if `values.yaml` exists in a `helm` directory, and contains the string `deploy: true` anywhere in the file  |

Note that any errors encountered while processing the expression are considered the same as if it had evaluated false.

## Plugins

This app supports arbitrary plugins for performing preprocessing on GitLab projects before adding them to Argo. If the environment variable `PLUGIN_DIRECTORY` is set, the directory will be scanned for Python files. Each Python file found in this directory is considered a single plugin, and should define a function with the signature `plugin(project) -> bool`. This is the plugin's entrypoint. It receives a parameter `project` of type `gitlab.v4.objects.Project` which is documented [here](https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html#reference). It should return a boolean value, indicating whether the project should be added to Argo or not. If any plugin returns false - the project is 'rejected' and not added to Argo (though it will be rescanned the next time the job is run). An example plugin file can be found in [plugins/example.py](plugins/example.py).

## Typical Deployment

```sh
cd helm
helm install my-bridge . \
--set "gitLab.apiUrl=https://gitlab.your-domain.com" \
--set "gitLab.personalAccessToken=1234567890" \
--set "gitLab.parentRepositoryID=1234" \
--set "resourcePrefix=autodetected-repo" \
--set "chartPath=where/helm/charts/live/in/new/repos" \
--set "sshSecretName=my-private-key-secret-name" \
--set "destinationNamespace=charts-get-deployed-here"
```

Or, with a condition: 

```sh
cd helm
helm install my-bridge . \
--set "gitLab.apiUrl=https://gitlab.your-domain.com" \
--set "gitLab.personalAccessToken=1234567890" \
--set "gitLab.parentRepositoryID=1234" \
--set "resourcePrefix=autodetected-repo" \
--set "chartPath=where/helm/charts/live/in/new/repos" \
--set "sshSecretName=my-private-key-secret-name" \
--set "destinationNamespace=charts-get-deployed-here" \
--set "processRepositoryCondition=exists('deploy.yaml')"
```