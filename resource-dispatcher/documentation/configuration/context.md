# Context

Each step in a task run occurs with one single, mutable _context_. The context is initialized as empty at the start of a task run, unless the task is triggered from a webhook with parameters - in which case, the context is initialized with those parameters. 

It is up to each individual plugin how the context should be used, and whether it is writable in any way, or read-only. The context is the only way (aside from writing to the filesystem) for a step to pass data to later steps.

Some examples of using context:

```yaml
tasks:
  - name: test
    triggers:
      - type: webhook
        route: /test
    steps:
      - plugin: script
        params:
          script: |
            context["stuff"] = "setting a context var"
      - plugin: script
        params:
          script: |
            print(f"The previous step told me: {context['stuff']}")
```

or:

```yaml
tasks:
  - name: test
    triggers:
      - type: webhook
        route: /test
    steps:
      - plugin: script
        params:
          script: |
            print(f"The webhook told me: {context['stuff']}")
```

```shell script
curl http://this-app/test?stuff=context_data
```

or:

```yaml
tasks:
  - name: test
    triggers:
      - type: webhook
        route: /test
    steps:
      - plugin: script
        params:
          script: |
            context["var_one"] = "input to an Ansible playbook"
      - plugin: ansible
        repository: automation-repo
        params:
          playbook_path: site.yml
          inventory_path: inventory
          extra_vars:
            # note that var_one is not defined here
            var_two: stuff
```

(since the `ansible` plugin automatically imports context vars as extra vars if they're not overridden by an explicit declaration in `extra_vars`)
