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
