# Concurrency

Two different tasks are able to run concurrently without interfering with each other (even if they depend on the same repositories).

Multiple runs of _the same task_ are not allowed by default, since this is probably undesirable. If a task is running and a second execution of that task is queued by the scheduler or by a webhook call, the second execution is immediately terminated (with a warning in the console) and no plugins are executed.

_Experimental_ concurrency of tasks can be enabled by setting `enable_concurrency: true` on the task.
