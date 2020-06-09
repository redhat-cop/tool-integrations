# Steps & Parameters

Each task is made up of at least one _step_. A step is an individual invocation of a plugin with certain parameters.

## Configuration

Step definitions almost always make use of a `params` input to tell them what to do:

```yaml
tasks:
  ...
    steps:
      - plugin: script
        params:
          script: |
            from os import listdir
            listdir(".")
```

However, note that steps may also make use of the task's [_context_](context.md) as input.

> :exclamation: **While there is filesystem persistence between steps in a task, there is _no filesystem persistence_ between separate task executions!** Each execution runs in an environment representative of a fresh clone of the Git repository, even if previous executions have written/modified/deleted any files.

## Runtime-Set Parameters

A step plugin can have its `params` set by data stored in the [_context_](context.md) instead of being explicitly written into the config YAML, if desired. The `params_from_context` option is used to enable this:

```yaml
tasks:
  - name: Example of params_from_context
    triggers:
      - type: webhook
        route: /test
    steps:
      - plugin: script
        params:
          script: |
            context["script_params"] = {"script": "print('Example output')"}
      - plugin: script
        params_from_context: script_params
```

In this example, the second `script` step would take its params from the `script_params` value of the context, which has a simple inline script containing one `print` statement. This is a powerful function for defining actions using data which is only determinable at runtime.

It is possible to specify both `params_from_context` _and_ `params` for a step. If this occurs, the two are merged at runtime, with `params` taking precedent in the event of a conflict.

## Looping

It is possible to configure a step to iterate over a list defined in the [_context_](context.md). This is configured by setting the `loop_over_context` option to the name of an iterable object in the context. That object in the context is then set to an _element_ of the list, and the step plugin is run for _each_ element found in that list. This is most easily explained by example. Take the following task definition:

```yaml
tasks:
  - name: Iteration example
    triggers:
      - type: webhook
        route: /test
    steps:
      - plugin: script
        params:
          script: |
            context["non_iterable_thing"] = "stuff"
            context["iterable_thing"] = [
              "First thing",
              "Second thing",
              "Third thing",
            ]
      - plugin: script
        loop_over_context: iterable_thing
        params:
          script: |
            print(context[iterable_thing])
```

The first `script` step sets the context to:

```json
{
  "non_iterable_thing": "stuff",
  "iterable_thing": [
    "First thing",
    "Second thing",
    "Third thing"
  ]
}
```

However, since the second `script` step specifies `loop_over_context: iterable_thing`, it is run _three times_, with the following three contexts:

```json
{
  "non_iterable_thing": "stuff",
  "iterable_thing": "First thing"
}
```

```json
{
  "non_iterable_thing": "stuff",
  "iterable_thing": "Second thing"
}
```

```json
{
  "non_iterable_thing": "stuff",
  "iterable_thing": "Third thing"
}
```

Thus, the task would print to the console:

```text
First thing
Second thing
Third thing
```

Despite this deconstruction of the iterable object; the context item being looped over, as well as all other non-iterated context items, are _still mutable_ - and any mutations are merged back into the original list. To demonstrate this, take the following task :

```yaml
tasks:
  - name: Iteration example
    triggers:
      - type: webhook
        route: /test
    steps:
      - plugin: script
        params:
          script: |
            context["mutation_counter"] = 0
            context["iterable_thing"] = [
              "First thing",
              "Second thing",
              "Third thing",
            ]
      - plugin: script
        loop_over_context: iterable_thing
        params:
          script: |
            context["mutation_counter"] = context["mutation_counter"] + 1
            context["iterable_thing"] = context["iterable_thing"] + " modified"
      - plugin: script
        params:
          script: |
            print(context)
```

which results in the context:

```json
{
  "mutation_counter": 3,
  "iterable_thing": [
    "First thing modified",
    "Second thing modified",
    "Third thing modified"
  ]
}
```

Looping **can** also be combined with the `params_from_context` configuration option described above. The following is a valid task definition:

```yaml
tasks:
  - name: Demonstrate runtime-set params with looping
    triggers:
      - type: webhook
        route: /test
    steps:
      - plugin: script
        params:
          script: |
            context["script_params"] = [
              {"script": "print('thing1')"},
              {"script": "print('thing2')"},
              {"script": "print('thing3')"},
            ]
      - plugin: script
        loop_over_context: script_params
        params_from_context: script_params
```

Which would print to the console:

```text
thing1
thing2
thing3
```

## Repository Scoping

If a step does not specify a `repository`, it is run in a working directory with _every repository_ available to it. For example, the task defined by the following YAML spec, with the following repository definition in the config file:

```yaml
repositories:
  - name: automation-repo-1
    url: https://github.com/my-org/some-ansible-playbooks.git
  - name: automation-repo-2
    url: https://github.com/my-org/some-ansible-playbooks-2.git

tasks:
    steps:
      - plugin: script
        params:
          script: |
            from os import listdir
            listdir(".")
```

Would see a directory structure like this:

```text
<current working directory>
├── automation-repo-1
│   ├── repo-file-1
│   ├── repo-file-2
├── automation-repo-2
│   ├── repo-file-1
│   ├── repo-file-2
```

<hr>

However, a step _scoped_ to a certain repository: 

```yaml
repositories:
  - name: automation-repo-1
    url: https://github.com/my-org/some-ansible-playbooks.git
  - name: automation-repo-2
    url: https://github.com/my-org/some-ansible-playbooks-2.git

tasks:
    steps:
      - plugin: script
        repository: automation-repo-2
        params:
          script: |
            from os import listdir
            listdir(".")
```

Would be executed inside of that repository directory:

```text
<current working directory (inside automation-repo-2)>
├── repo-file-1
├── repo-file-2
```

Steps may also make use of an additional `path` input to scope the execution of that step to a subdirectory of the repository: 

```yaml
repositories:
  - name: automation-repo-1
    url: https://github.com/my-org/some-ansible-playbooks.git
  - name: automation-repo-2
    url: https://github.com/my-org/some-ansible-playbooks-2.git

tasks:
    steps:
      - plugin: script
        repository: automation-repo-2
        path: some-subdirectory
        params:
          script: |
            from os import listdir
            listdir(".")
```
