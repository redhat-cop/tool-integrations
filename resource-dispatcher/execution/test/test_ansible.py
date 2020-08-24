import pytest
import execution
import os

def test_basic_ansible(capsys):
    task = {
        "name": "Ansible Test",
        "disable_error_handling": True,
        "steps": [
            {
                "plugin": "ansible",
                "params": {
                    "playbook_path": os.getcwd() + "/execution/test/test_playbook/site.yml",
                    "inventory_path": os.getcwd() + "/execution/test/test_playbook/inventory"
                }
            }
        ]
    }
    
    execution.task_function(task, context={})

    captured = capsys.readouterr()
    assert "Hello, world!" in captured.out