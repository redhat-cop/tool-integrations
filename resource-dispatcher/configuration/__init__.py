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
        f = open(os.environ["CONFIG_FILE"], "r")
        contents = f.read()
        f.close()
        contents_template = Template(contents)
        templated_contents = contents_template.render(**template_vars)
        configuration = yaml.load(templated_contents, Loader=yaml.FullLoader)
        print(f"Loaded configuration file: {f.name}")
        return configuration

    if mode == "dir":
        configuration = {
            "repositories": [],
            "tasks": []
        }
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
        return configuration
