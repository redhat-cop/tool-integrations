import pytest
import execution
import os

def test_ansible_basic(capsys):
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


def test_ansible_reading_context(capsys):
    task = {
        "name": "Ansible Test",
        "disable_error_handling": True,
        "steps": [
            {
                "plugin": "script",
                "params": {
                    "script": "context['test_var'] = 'Set via context!'"
                }
            },
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
    assert "Set via context!" in captured.out


def test_ansible_merging_params_from_context(capsys):
    task = {
        "name": "Ansible Test",
        "disable_error_handling": True,
        "steps": [
            {
                "plugin": "script",
                "params": {
                    "script": "context['test_var'] = {'extra_vars': {'test_var_1': 'thing1'}}"
                }
            },
            {
                "plugin": "ansible",
                "params_from_context": "test_var",
                "params": {
                    "playbook_path": os.getcwd() + "/execution/test/test_playbook/site.yml",
                    "inventory_path": os.getcwd() + "/execution/test/test_playbook/inventory",
                    "extra_vars": {
                        "test_var_2": "thing2"
                    }
                }
            }
        ]
    }
    
    execution.task_function(task, context={})

    captured = capsys.readouterr()
    assert "thing1" in captured.out
    assert "thing2" in captured.out