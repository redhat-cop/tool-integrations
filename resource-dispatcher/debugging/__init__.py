from mem_top import mem_top
from triggering.scheduled import generate_schedule_fn
from pathlib import Path
import psutil
import os
import time

def configure_debugging(debug_config):
    if "memory_profile" in debug_config:
        fn = generate_schedule_fn(debug_config["memory_profile"]["interval"])
        fn.do(print_memory_profile)
        print("Configured memory profiler")
    if "pid_profile" in debug_config:
        fn = generate_schedule_fn(debug_config["pid_profile"]["interval"])
        fn.do(print_pid_profile)
        print("Configured PID profiler")
    if "disk_profile" in debug_config:
        fn = generate_schedule_fn(debug_config["disk_profile"]["interval"])
        fn.do(print_disk_profile)
        print("Configured disk profiler")

def print_memory_profile():
    print("\n### DEBUG: BEGIN MEMORY PROFILE ###\n")
    print(mem_top())
    print("\n### DEBUG: END MEMORY PROFILE ###\n")

def print_pid_profile():
    children = psutil.Process().children(recursive=True)
    zombies = list(child for child in children if child.status() is psutil.STATUS_ZOMBIE)
    print("\n### DEBUG: BEGIN PID PROFILE ###\n")
    if len(children) > 0:
        pids = ", ".join([str(child.pid) for child in children])
        current_time = time.time()
        created = ", ".join([str(round(current_time - child.create_time())) for child in children])
        print(f"There are {len(children)} child processes. PIDs are: {pids} - spawned {created} seconds ago, respectively")
    else:
        print("There are no child processes.")
    if len(zombies) > 0:
        pids = ", ".join([str(child.pid) for child in zombies])
        print(f"{len(zombies)} are zombie processes. PIDs are: {pids}")
    else:
        print("None are zombie processes.")
    print("\n### DEBUG: END PID PROFILE ###\n")

def print_disk_profile():
    print("\n### DEBUG: BEGIN DISK PROFILE ###\n")
    if os.path.exists("tmp"):
        cache_size = sum(file.stat().st_size for file in Path("tmp").rglob('*'))
        print(f"Repository cache: {cache_size} bytes")
    else:
        print("Repository cache does not exist.")
    children = psutil.Process().children(recursive=True)
    tmp_directories = {(child.pid, child.cwd()) for child in children if child.status() is not psutil.STATUS_ZOMBIE}
    if len(tmp_directories) > 0:
        for directory in tmp_directories:
            size = sum(file.stat().st_size for file in Path(directory[1]).rglob('*'))
            print(f"Temporary directory in use by PID {directory[0]}: {directory[1]} ({size} bytes)")
    else:
        print("No temporary directories in use.")
    open_files = psutil.Process().open_files()
    if len(open_files) > 0:
        print(f"Other open files: {open_files}")
    else:
        print("No other open files.")
    print("\n### DEBUG: END DISK PROFILE ###\n")