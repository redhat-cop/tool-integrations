import os
import yaml
import sys
from jinja2 import Template


def get_config():
    # The system management supervisor `execute_supervised` will not let us get here unless exactly one of these is defined.
    if "CONFIG_DIR" in os.environ:
        mode = "dir"
    elif "CONFIG_FILE" in os.environ:
        mode = "file"

    template_vars = {"ENV_" + var: os.environ[var] for var in os.environ}

    if mode == "file":
        if not os.environ["CONFIG_FILE"].endswith(".yml") and not os.environ["CONFIG_FILE"].endswith(".yaml"):
            print("Configuration file must be in *.yml or *.yaml format.")
            raise Exception("Configuration file not in required format")
        f = open(os.environ["CONFIG_FILE"], "r")
        contents = f.read()
        f.close()
        contents_template = Template(contents)
        templated_contents = contents_template.render(**template_vars)
        configuration = yaml.load(templated_contents, Loader=yaml.FullLoader)
        print(f"Loaded single configuration file: {f.name}")
        config_structure_warnings(os.environ["CONFIG_FILE"], configuration)
        return configuration

    if mode == "dir":
        configuration = {
            "repositories": [],
            "tasks": []
        }
        print(f"Looking for configuration files in directory: {os.environ['CONFIG_DIR']}")
        for file in os.listdir(os.environ["CONFIG_DIR"]):
            if file.endswith(".yml") or file.endswith(".yaml"):
                path = os.path.join(os.environ["CONFIG_DIR"], file)
                f = open(path, "r")
                contents = f.read()
                f.close()
                contents_template = Template(contents)
                templated_contents = contents_template.render(**template_vars)
                config_tmp = yaml.load(templated_contents, Loader=yaml.FullLoader)
                config_merge(configuration, config_tmp)
                print(f"Found configuration file: {path}")
                config_structure_warnings(path, config_tmp)
            else:
                print(f"Skipping file (not *.yml or *.yaml): {os.path.join(os.environ['CONFIG_DIR'], file)}")
        return configuration


def config_merge(existing_config, new_config):
    if "repositories" in new_config:
        for repository in new_config["repositories"]:
            # Check if an _exact_ match has already been defined somewhere else
            if repository not in existing_config["repositories"]:
                if repository["name"] in [existing_repo["name"] for existing_repo in existing_config["repositories"]]:
                    # A repo with the same name but different characteristics has already been defined. Error.
                    raise Exception(f"A repository named {repository['name']} has already been defined. Cannot proceed with configuration.")
                ref = repository["ref"] if "ref" in repository else "master"
                if (repository["url"], ref) in [(existing_repo["url"], existing_repo["ref"] if "ref" in existing_repo else "master") for existing_repo in existing_config["repositories"]]:
                    # A repo with a different name but the same characteristics has already been defined. Warning.
                    print(f"Warning: The same repository has been defined twice with different names. Consider refactoring config to reduce duplication: {repository['url']}")
                existing_config["repositories"].append(repository)
            # No else clause here - if the repository has already been defined with exactly
            # the same characteristics, we don't really have a problem.
            # Just ignore the second one.
    if "tasks" in new_config:
        for task in new_config["tasks"]:
            if task["name"] in [existing_task["name"] for existing_task in existing_config["tasks"]]:
                raise Exception(f"A task named {task['name']} has already been defined. Cannot proceed with configuration.")
            new_routes = {trigger["route"] for trigger in task["triggers"] if trigger["type"] == "webhook"}
            existing_triggers = [existing_task["triggers"] for existing_task in existing_config["tasks"]]
            existing_triggers_flattened = [trigger for triggers in existing_triggers for trigger in triggers] # turn list of lists of triggers into single list of triggers
            existing_routes = {trigger["route"] for trigger in existing_triggers_flattened if trigger["type"] == "webhook"}
            intersection = new_routes.intersection(existing_routes)
            if intersection:
                raise Exception(f"A webhook route collision has been detected. Cannot proceed with configuration: {intersection}")
            existing_config["tasks"].append(task)


def config_structure_warnings(filename, config):
    keys_defined = set(config.keys())
    keys_understood = {"repositories", "tasks"}
    extra_keys = keys_defined.difference(keys_understood)
    if len(extra_keys):
        print(f"Warning: Fields defined in configuration file but not used: {extra_keys}")
    pass