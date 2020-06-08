# Ansible Plugin

The Ansible plugin executes an Ansible playbook against an inventory, both intended to be pulled in from a Git repository.

## Parameters

| Parameter | Description | Required | Default |
|---|---|---|---|
| `playbook_path` | The path to the playbook to execute | True | N/A |
| `inventory_path` | The path to the inventory that the playbook should be executed against | True | N/A |
| `extra_vars` | A dictionary of any extra values to be passed to the playbook execution | False | `null` |

## How Context Is Used

This plugin pulls in the context as extra variables to the playbook run. Variables set in the `extra_vars` parameter option override any values found in the context with the same name.

This plugin does not write back to the context.

## Example Usages

Playbook and inventory in the same repository:

```yaml
repositories:
  - name: gitlab-to-argo-repo
    url: https://github.com/jacobsee/gitlab_to_argo.git

tasks:
  - name: gitlab-to-argo
    description: Ensures that all repositories in a GitLab group are being watched by an Argo CD instance
    triggers:
      - type: webhook
        route: /do_stuff
    steps:
      - plugin: ansible
        repository: gitlab-to-argo-repo
        params:
          playbook_path: site.yml
          inventory_path: inventory
          extra_vars:
            gitlab_base_url: https://gitlab.com
            gitlab_group: 1234
            gitlab_private_token: 123456
```

Playbook and inventory in the different repositories:

```yaml
repositories:
  - name: first-repo
    url: https://github.com/jacobsee/first-repo.git
  - name: second-repo
    url: https://github.com/jacobsee/second-repo.git

tasks:
  - name: gitlab-to-argo
    description: Ensures that all repositories in a GitLab group are being watched by an Argo CD instance
    triggers:
      - type: webhook
        route: /do_stuff
    steps:
      - plugin: ansible
        params:
          playbook_path: first-repo/site.yml
          inventory_path: second-repo/inventory
```
