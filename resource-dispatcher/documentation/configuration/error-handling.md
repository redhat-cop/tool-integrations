# Error Handling

By default, tasks are entirely wrapped in error handlers so that any uncaught errors arising from any step plugins do not allow the system to crash or otherwise impact any other running tasks.

This behavior can be disabled on a per-task basis for debugging purposes, as Python may print more descriptive error messages and a helpful stack trace during a crash if the error is uncaught by this handler. **DO NOT DO THIS FOR A TASK RUNNING IN A PRODUCTION ENVIRONMENT!**

To disable task error handling, add the `disable_error_handling: true` statement to the task definition:

```yaml
tasks:
  - name: Run a script
    description: Runs a script with an error
    disable_error_handling: true
    triggers:
      - type: scheduled
        every: 5 minutes
    steps:
      - plugin: script
        params:
          script: |
            raise Exception("Something is broken!")
```
