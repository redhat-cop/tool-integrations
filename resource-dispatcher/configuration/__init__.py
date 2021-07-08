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
        config_warnings(os.environ["CONFIG_FILE"], configuration)
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
                if "repositories" in config_tmp:
                    configuration["repositories"].extend(config_tmp["repositories"])
                if "tasks" in config_tmp:
                    configuration["tasks"].extend(config_tmp["tasks"])
                print(f"Found configuration file: {path}")
                config_warnings(path, config_tmp)
            else:
                print(f"Skipping file (not *.yml or *.yaml): {os.path.join(os.environ['CONFIG_DIR'], file)}")
        return configuration


def config_warnings(filename, config):
    keys_defined = set(config.keys())
    keys_understood = {"repositories", "tasks"}
    extra_keys = keys_defined.difference(keys_understood)
    if len(extra_keys):
        print(f"Warning: Fields defined in configuration file but not used: {extra_keys}")
    pass