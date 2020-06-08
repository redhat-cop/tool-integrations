# Repositories

Unless you compose task workflow entirely out of plugins with inline configuration/scripts, you will likely need to pull in existing resources to accomplish your goals, for example: an Ansible playbook & inventory are required to use the Ansible plugin.

These repositories are defined in the config file like this:

```yaml
repositories:
  - name: automation-repo-1
    url: git@github.com:my-org/some-ansible-playbooks.git
    secret:
      ssh_private_key: /my/path/to/an/ssh/key
  - name: automation-repo-2
    url: https://github.com/my-org/some-ansible-playbooks-2.git
```

Upon application startup, these repositories are cloned. They can be referenced from that point forward by their name as defined here, _not_ by any part of their Git URL.

**The same scheduling mechanism used to trigger tasks is _automatically configured_ to pull new changes from these repositories every two minutes, so updates to these dependencies should be picked up _without any user intervention required_.**
