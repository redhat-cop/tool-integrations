import time
from triggering.scheduled import schedule_trigger, run as run_scheduled
from triggering.webhook import WebHook

use_webhook_triggers = False


def configure_triggers(task, job):
    global use_webhook_triggers
    for trigger in task["triggers"]:
        if trigger["type"] == "scheduled":
            schedule_trigger(task["name"], trigger, job)
            print(f"Configured scheduler for task {task['name']}")
        elif trigger["type"] == "webhook":
            webhook = WebHook()
            webhook.add(task["name"], trigger["route"], job)
            use_webhook_triggers = True
            print(f"Configured webhook handler for task {task['name']}")


def start():
    global use_webhook_triggers
    if use_webhook_triggers:
        print("Webhook handlers have been configured... spawning webserver thread.")
        webhook = WebHook()
        webhook.listen()
    else:
        print("No webhook triggers detected... Skipping webserver initialization.")
    print()
    print("---------------------------------------------")
    print("Configuration is complete - tasks are active.")
    print("---------------------------------------------")
    print()
    while True:
        run_scheduled()
        time.sleep(1)
