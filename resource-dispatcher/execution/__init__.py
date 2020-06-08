import tempfile
import shutil
import importlib
import threading
import os
from copy import copy
from execution.cd import cd
from threading import Lock


def initialize(task):
    for step in task["steps"]:
        plugin = importlib.import_module('execution.plugins.' + step["plugin"])
        if "params_from_context" in step and "params" not in step:
            step["params"] = {}
        if hasattr(plugin, "initialize") and callable(plugin.initialize):
            print(f"Initializing plugin {step['plugin']}")
            if "repository" in step and "path" in step and os.path.isdir(step["repository"] + "/" + step["path"]):
                with cd(step["repository"] + "/" + step["path"]):
                    plugin.initialize(step["params"])
            elif "repository" in step and os.path.isdir(step["repository"]):
                with cd(step["repository"]):
                    plugin.initialize(step["params"])
            else:
                plugin.initialize(step["params"])


def build_task(task):

    @multithread
    @determine_concurrency_mode(task)
    @handle_errors(task)
    def task_function(context={}):
        with tempfile.TemporaryDirectory() as temp_dir:
            for repository in [f.name for f in os.scandir("tmp") if f.is_dir()]:
                shutil.copytree("tmp/" + repository, temp_dir + "/" + repository)
            with cd(temp_dir):
                for step in task["steps"]:
                    # Load necessary execution plugin
                    plugin = importlib.import_module('execution.plugins.' + step["plugin"])
                    # Set runtime directory properly for the step to execute
                    if "repository" in step and "path" in step:
                        with cd(step["repository"] + "/" + step["path"]):
                            result = execute_step(plugin.process, step, context)
                    elif "repository" in step:
                        with cd(step["repository"]):
                            result = execute_step(plugin.process, step, context)
                    else:
                        result = execute_step(plugin.process, step, context)

                    if (isinstance(result, bool) and result is False) or (isinstance(result, dict) and result["pass"] is False):
                        print("Step has broken execution - halting task")
                        break

    return task_function


def execute_step(fn, step, context):
    loop_over = step["loop_over_context"] if "loop_over_context" in step else None
    if loop_over is None:
        constructed_params = {}
        if "params_from_context" in step:
            constructed_params.update(context[step["params_from_context"]])
        if "params" in step:
            constructed_params.update(step["params"])
        return fn(context, constructed_params)
    else:
        if isinstance(context[loop_over], list):
            # List to be merged _back into_ the context
            loop_list = copy(context[loop_over])

            for index, element in enumerate(context[loop_over]):
                # Copy the dictionary and replace the iterable item with a single element
                context_copy = copy(context)
                context_copy.update({loop_over: element})
                # Construct parameters for this run
                constructed_params = {}
                if "params_from_context" in step:
                    constructed_params.update(context_copy[step["params_from_context"]])
                if "params" in step:
                    constructed_params.update(step["params"])
                # Run step
                fn(context_copy, constructed_params)
                # Write (potentially) modified list element back to the loop_list
                loop_list[index] = copy(context_copy[loop_over])
                # Write all the rest of the context variables back to the global context
                del context_copy[loop_over]
                context.update(context_copy)
            # Update context with the loop_list
            context.update({loop_over: loop_list})
            return True
        else:
            raise Exception("Error: Tried to loop over a non-iterable context object.")


def multithread(fn):
    def run_threaded(*args, **kwargs):
        job_thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        job_thread.start()
    return run_threaded


def determine_concurrency_mode(task):
    if "enable_concurrency" in task and task["enable_concurrency"] is True:
        def handle_concurrency(fn):
            def enable_concurrency(*args, **kwargs):
                fn(*args, **kwargs)
            return enable_concurrency
    else:
        def handle_concurrency(fn):
            mutex = Lock()

            def restrict_concurrency(*args, **kwargs):
                if mutex.acquire(False):
                    try:
                        return fn(*args, **kwargs)
                    finally:
                        mutex.release()
                else:
                    print("Task aborted - Another instance is already running and concurrency has not been enabled")
            return restrict_concurrency
    return handle_concurrency


def handle_errors(task):

    if "disable_error_handling" in task and task["disable_error_handling"]:
        def handler(fn):
            def f(*args, **kwargs):
                fn(*args, **kwargs)
            return f
    else:
        def handler(fn):
            def f(*args, **kwargs):
                try:
                    fn(*args, **kwargs)
                except Exception as e:
                    print(f"ERROR EXECUTING TASK {task['name']}:")
                    print(str(e))

            return f
    return handler
