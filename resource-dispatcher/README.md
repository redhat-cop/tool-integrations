# Resource Dispatcher

Integration composition and triggering mechanism designed to take advantage of existing tools and scripts.

**The documentation for deploying, configuring, and using the tool can be [found here](documentation/README.md).**

### <a name="hdiw"></a>How Does It Work?

It takes a single configuration file (which is watched and live-reloaded) containing:

* A number of tasks
* A list of repositories that those tasks depend on
* A set of triggers defining when those tasks should be run


Here is simple workflow demonstrating all of these things:

```yaml
repositories:
  - name: automation-repo
    url: https://github.com/my-org/some-ansible-playbooks.git

tasks:
  - name: Run my Ansible playbook
    description: Runs an Ansible playbook under a number of trigger scenarios
    triggers:
      - type: scheduled
        every: 2 hours
      - type: scheduled
        every: thursday
        at: "15:30"
      - type: webhook
        route: /do_a_thing
    steps:
      - plugin: ansible
        repository: automation-repo
        params:
          playbook_path: site.yml
          inventory_path: inventory
```

In this case, we have pulled in one repository (`https://github.com/my-org/some-ansible-playbooks.git`) and scheduled a task which executes a playbook in that repository every 2 hours, every Thursday at 3:30PM, and every time a webhook at the route `/do_a_thing` is called by some other service.

This is a very simple example of a task definition. You can see more examples in the documentation of how task definitions can be used to string together more complicated logic.
