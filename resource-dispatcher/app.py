from configuration import get_config
from repositories import configure_repository
from execution import build_task, initialize
from triggering import configure_triggers, start
from system_management import execute_supervised
from debugging import configure_debugging


def main():
    config = get_config()

    for repository in config["repositories"]:
        configure_repository(repository)

    for task in config["tasks"]:
        initialize(task)
        task_function = build_task(task)
        configure_triggers(task, task_function)

    if "debugging" in config:
        configure_debugging(config["debugging"])

    start()


if __name__ == "__main__":
    execute_supervised(main)
