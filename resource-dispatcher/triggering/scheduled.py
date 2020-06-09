import sys
import schedule
import datetime


def schedule_trigger(name, trigger, job):
    timing = trigger["every"].split()
    wrapped_job = __wrap_job(name, job)
    if len(timing) == 1:
        fn = getattr(schedule.every(), timing[0])
    elif len(timing) == 2:
        fn = getattr(schedule.every(int(timing[0])), timing[1])
    else:
        sys.exit(f"Failed to parse the schedule: {trigger['every']}")

    if "at" in trigger:
        fn.at(trigger["at"]).do(wrapped_job)
    else:
        fn.do(wrapped_job)


def __wrap_job(name, job):
    def wrapped_job():
        print(f"Scheduler is executing task {name} at {datetime.datetime.now()}")
        job()
    return wrapped_job


def run():
    schedule.run_pending()
