import json
import requests

def process(ctx, params):
    towerVars = params
    if "tower" in ctx:
        deep_merge(towerVars, ctx["tower"])

    # Set up all the things that Tower wants
    session = requests.Session()
    session.auth = (towerVars["username"], towerVars["password"])
    session.headers.update({"Content-Type": "application/json"})

    # Look up job names & IDs
    r = session.get(f"{towerVars['url']}/api/v2/job_templates/")
    if r.status_code < 200 or r.status_code >= 300:
        raise Exception(f"Error fetching Tower job template list: {str(r.content)}")
    template_map = {result["name"]: result["id"] for result in r.json()["results"]}
    if towerVars["job_template"] not in template_map:
        raise Exception(f"Ansible Tower job template \"{towerVars['job_template']}\" not found on the remote server")
    print(f"Found job template \"{towerVars['job_template']}\" - launching now")

    # Execute job
    extra_vars = towerVars["extra_vars"] if "extra_vars" in towerVars else {}
    r = session.post(f"{towerVars['url']}/api/v2/job_templates/{template_map[towerVars['job_template']]}/launch/", json={"extra_vars": json.dumps(extra_vars, separators=(',', ':'))})
    if r.status_code < 200 or r.status_code >= 300:
        raise Exception(f"Error launching Ansible Tower job: {str(r.content)}")
    if "extra_vars" in r.json()["ignored_fields"]:
        print("WARNING: Extra vars were specified, but Ansible Tower did not accept them. Ensure that \"Prompt for extra_vars\" is enabled on the job template.")
    print(f"Launched Ansible Tower job with ID: {r.json()['id']}")

def deep_merge(merge_into, merge_from, path=None):
    if path is None: path = []
    for key in merge_from:
        if key in merge_into:
            if isinstance(merge_from[key], dict) and isinstance(merge_into[key], dict):
                deep_merge(merge_into[key], merge_from[key], path + [str(key)])
            elif merge_into[key] == merge_from[key]:
                pass
            else:
                raise Exception('Cannot merge dictionary with non-dictionary element: %s' % '.'.join(path + [str(key)]))
        else:
            merge_into[key] = merge_from[key]
