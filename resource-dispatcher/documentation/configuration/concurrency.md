# Concurrency

Two different tasks are able to run concurrently without interfering with each other (even if they depend on the same repositories).

Multiple runs of _the same task_ are not currently allowed, since this is probably undesirable. If a task is running and a second execution of that task is queued by the scheduler or by a webhook call, the second execution is immediately terminated (with a warning in the console) and no plugins are executed.

TODO: Make this configurable per-task since it's not really a technical limitation at all.
