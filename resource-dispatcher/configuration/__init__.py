import os
import yaml
import sys


def get_config():
    if "CONFIG_FILE" not in os.environ:
        sys.exit("Environment variable CONFIG_FILE must be defined or this application has nothing to do. Exiting.")
    f = open(os.environ["CONFIG_FILE"], "r")
    contents = f.read()
    f.close()
    configuration = yaml.load(contents, Loader=yaml.FullLoader)
    return configuration
