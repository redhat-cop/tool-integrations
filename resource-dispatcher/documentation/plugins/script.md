# Script Plugin

The script plugin runs a Python script from either an inline definition in the YAML, or a `.py` file.

## Parameters

| Parameter | Description | Required | Default |
|---|---|---|---|
| `script` | An inline script to execute | False | N/A |
| `script_file` | The path to a `.py` file to execute | False | N/A |

_Either_ `script` or `script_file` are required.

## How Context Is Used

`context` is available as a readable/writable dictionary within the scripts.

## Example Usages

This plugin wraps the provided script inside of a function, so that `return` is available as a keyword. If a script returns `False`, or a dict containing `{"pass": False}` the execution of the entire task is halted.

Using a script file:

```yaml
repositories:
  - name: repo
    url: https://github.com/jacobsee/gitlab_to_argo.git

tasks:
  - name: scripto
    description: Script plugin example
    triggers:
      - type: webhook
        route: /do_stuff
    steps:
      - plugin: script
        repository: repo
        params:
          script_file: app.py
```

Inline script referencing `context`:

```yaml
tasks:
  - name: scripto
    description: Script plugin example
    triggers:
      - type: webhook
        route: /do_stuff
    steps:
      - plugin: script
        params:
          script: |
            print(f"An existing context var is {context['input']}")
            context["input"] = "and now we're setting it to this
            return False # For example, something broke here, so we'll stop other steps from running
```
