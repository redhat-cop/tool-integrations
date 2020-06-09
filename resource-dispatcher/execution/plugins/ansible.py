from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.playbook import play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import yaml
import json


def process(ctx, params):
    playbook_path = params["playbook_path"] if "playbook_path" in params else "site.yml"
    inventory_path = params["inventory_path"] if "inventory_path" in params else "inventory/hosts"
    connection = params["connection"] if "connection" in params else "local"
    become = params["become"] if "become" in params else None
    become_method = params["become_method"] if "become_method" in params else None
    become_user = params["become_user"] if "become_user" in params else None
    extra_vars = dict(ctx)
    if "extra_vars" in params:
        extra_vars.update(params["extra_vars"])

    loader = DataLoader()
    passwords = dict(vault_pass=params["vault_password"] if "vault_password" in params else "")

    context.CLIARGS = ImmutableDict(connection=connection, module_path=['.'], forks=10, become=become,
                                    become_method=become_method, become_user=become_user, check=False, diff=False)
    # results_callback = ResultCallback()
    inventory = InventoryManager(loader=loader, sources=[inventory_path])
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    with open(playbook_path, 'r') as file:
        playbook_str = file.read()
    playbook_data = yaml.load(playbook_str, Loader=yaml.FullLoader)
    plays = [play.Play().load(data=play_data, variable_manager=variable_manager, loader=loader, vars=extra_vars) for play_data in playbook_data]

    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            passwords=passwords,
            # stdout_callback=results_callback,
            # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
        )
        for play_data in plays:
            result = tqm.run(play_data)
    finally:
        if tqm is not None:
            tqm.cleanup()


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(result._result)
        # print(json.dumps({host.name: result._result}, indent=4))
