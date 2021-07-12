from multiprocessing import Process
import time
import hashlib
import signal
import sys
import os
import shutil


main_job = None


def terminate(*args):
    global main_job
    if main_job is not None:
        print("[System Management] Terminating task engine")
        main_job.kill()
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
    main_job = None


def terminate_and_exit(*args):
    terminate(args)
    sys.exit(0)


def hash(file):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(file, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


def hash_directory(path):
    hashes = set()
    for file in os.listdir(os.environ["CONFIG_DIR"]):
        if file.endswith(".yml") or file.endswith(".yaml"):
            hashes.add(hash(os.path.join(os.environ["CONFIG_DIR"], file)))
    return hashes


def execute_supervised(process):
    global main_job
    signal.signal(signal.SIGTERM, terminate_and_exit)
    signal.signal(signal.SIGINT, terminate_and_exit)
    while True:
        print("[System Management] Spawning new task engine")
        if "CONFIG_FILE" not in os.environ and 'CONFIG_DIR' not in os.environ:
            sys.exit("Environment variable CONFIG_FILE or CONFIG_DIR must be defined or this application has nothing to do. Exiting.")
        elif "CONFIG_FILE" in os.environ and 'CONFIG_DIR' in os.environ:
            sys.exit("Both environment variables CONFIG_FILE and CONFIG_DIR are defined but only one is supported at a time. Exiting.")
        if "ENABLE_TRIGGERING" in os.environ and os.environ["ENABLE_TRIGGERING"].lower() == "false":
            print("[System Management] Triggering is disabled by environment variable - halting here as the task engine has no work to do")
            time.sleep(300)
            sys.exit(0)
        main_process = Process(target=process)
        main_process.start()
        main_job = main_process
        if "CONFIG_FILE" in os.environ:
            current_hash = hash(os.environ["CONFIG_FILE"])
            while hash(os.environ["CONFIG_FILE"]) == current_hash:
                time.sleep(15)
        elif "CONFIG_DIR" in os.environ:
            current_hashes = hash_directory(os.environ["CONFIG_DIR"])
            while hash_directory(os.environ["CONFIG_DIR"]) == current_hashes:
                time.sleep(15)
        print("[System Management] Configuration has been modified - Restarting")
        terminate()
        time.sleep(1)
