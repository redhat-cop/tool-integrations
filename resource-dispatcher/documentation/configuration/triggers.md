# Triggers

All tasks definitions require a `triggers` block, else the task would never be able to execute and thus the definition would be useless. Multiple triggers can be defined for the same task. Two kinds of triggers are currently supported: Schedule, and Webhook.

## Schedule

Schedule triggers execute a task periodically based on a time condition, and can take a number of forms:

```yaml
tasks:
  ...
    triggers:
      - type: scheduled
        every: minute
```

```yaml
tasks:
  ...
    triggers:
      - type: scheduled
        every: 3 hours
```

```yaml
tasks:
  ...
    triggers:
      - type: scheduled
        every: thursday
        at: "15:30"
```

The following interval keywords are available to use in the `every` statement:


* second
* seconds
* minute
* minutes
* hour
* hours
* day
* days
* week
* weeks
* monday
* tuesday
* wednesday
* thursday
* friday
* saturday
* sunday

## Webhook

Webhook triggers configure the app to listen for a `GET` or `POST` request on a certain route. Whenever a request is encountered, the task is run. For example:
 
```yaml
tasks:
  ...
    triggers:
      - type: webhook
        route: /run_task_x
``` 
 
Webhook triggers allow for slightly more advanced execution, in that **webhook-triggered tasks can receive external inputs**. Any URL parameters received as a part of a `GET` request or form parameters received as a part of a `POST` request are parsed and added to the _task execution context_. Additionally, data posted with the header `Content-Type: application/json` will be decoded automatically before being written to the context.

ex. `curl "https://my-app-url/run_task_x?param1=stuff&param2=things"`

or `curl "https://my-app-url/run_task_x" -XPOST -d "param1=stuff" -d "param2=things"`

or `curl "https://my-app-url/run_task_x" -XPOST --header "Content-Type: application/json" -d '{"param1": "stuff", "param2": "things"}'`

See [context](context.md)

> :exclamation: **The internal webserver is only started if at least one task defines a webhook trigger.** If no tasks have a webhook trigger defined, server initialization is skipped entirely.