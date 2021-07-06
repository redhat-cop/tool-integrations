# Templating & Environment Vars

Configuration files, whether defined by `CONFIG_FILE` or `CONFIG_DIR`, are processed by the Jinja templating engine before parsing as YAML. This allows secrets and environment-specific data to be externalized from the YAML configurations and supplied by the environment at runtime.

To take advantage of this - use Jinja templating directly in the YAML. All environment variables present at runtime are available with an `ENV_` prefix. For example, to inject the contents of environment variables called `USERNAME` and `PASSWORD`:

```yaml
tasks:
  - name: Run a task
    description: Runs a task
    triggers:
      - type: scheduled
        every: 5 minutes
    steps:
      - plugin: ansible-tower
        params:
          url: "https://ansible-tower.my-domain.com"
          username: "{{ ENV_USERNAME }}"
          password: "{{ ENV_PASSWORD }}"
          job_template: "hello-world"
```

> :exclamation: **Note:** This will consume all Jinja-formatted variables defined in the config file. If this behavior is not intended and you wish for Jinja template-like content to be available at runtime, you will need to use [Jinja Escaping](https://jinja.palletsprojects.com/en/3.0.x/templates/#escaping) - for example with `{% raw %}` tags.

```yaml
tasks:
  - name: Run a task
    description: Runs a task
    triggers:
      - type: scheduled
        every: 5 minutes
    steps:
      - plugin: script
        params:
          script: |
{% raw -%}
            print("I want to have this {{ VARIABLE }} here at runtime!")
{% endraw %}
```
