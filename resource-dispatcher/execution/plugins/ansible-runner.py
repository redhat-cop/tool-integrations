import ansible_runner
import os


def process(ctx, params):
    playbook_path = params["playbook_path"] if "playbook_path" in params else "site.yml"
    private_data_dir= os.getcwd()
    inventory_path = (
        params["inventory_path"] if "inventory_path" in params else "inventory/hosts"
    )
    extra_vars = dict(ctx)
    if "extra_vars" in params:
        extra_vars.update(params["extra_vars"])
        # Use the Python that we're running as by default, so dependencies are available
        if "ansible_python_interpreter" not in params["extra_vars"]:
            extra_vars.update({"ansible_python_interpreter": "/opt/app-root/bin/python"})

    passwords = dict(
        vault_pass=params["vault_password"] if "vault_password" in params else ""
    )

    r = ansible_runner.run(
        private_data_dir=private_data_dir,
        inventory=inventory_path,
        playbook=playbook_path,
        extravars=extra_vars,
        passwords=passwords,
    )

    print("{}: {}".format(r.status, r.rc))
    print(f'Final status: {r.stats}')
