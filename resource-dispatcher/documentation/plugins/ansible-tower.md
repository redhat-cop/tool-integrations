# Ansible Tower Plugin

The Ansible Tower plugin launches a named job template on an Ansible Tower instance, optionally passing in additional `extra_vars`.

## Parameters

| Parameter | Description | Required | Default |
|---|---|---|---|
| `url` | The base URL of the Ansible Tower instance | True | N/A |
| `username` | The username to use for authentication to the Ansible Tower instance | True | N/A |
| `password` | The password to use for authentication to the Ansible Tower instance | True | N/A |
| `job_template` | The name of the job template to launch | True | N/A |
| `extra_vars` | A dictionary of any extra values to be passed to the playbook execution | False | `{}` |

## How Context Is Used

This plugin pulls in any variables in the context path `tower.extra_vars` as extra variables to the job run. Variables set in the `extra_vars` parameter option are deep merged with the context.

This plugin does not write back to the context.

## Example Usage

```yaml
repositories: {}

tasks:
  - name: my-tower
    description: Example Ansible Tower launch job
    triggers:
      - type: scheduled
        every: 10 seconds
    steps:
      - plugin: ansible-tower
        params:
          url: "https://ansible-tower.my-domain.com"
          username: admin
          password: password
          job_template: hello-world-job-template
          extra_vars:
            thing1: thing2
            thing3:
              - thing4
              - thing5
              - thing6

```
