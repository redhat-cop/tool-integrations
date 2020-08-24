import pytest
import execution


def test_script(capsys):
    task = {
        "name": "Script Test",
        "disable_error_handling": True,
        "steps": [
            {
                "plugin": "script",
                "params": {
                    "script": "print(\"Hello, world!\")"
                }
            }
        ]
    }
    
    execution.task_function(task, context={})

    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\n"


def test_script_with_context(capsys):
    task = {
        "name": "Script Test",
        "disable_error_handling": True,
        "steps": [
            {
                "plugin": "script",
                "params": {
                    "script": "print(f\"Hello, {context['input']}!\")"
                }
            }
        ]
    }
    
    execution.task_function(task, context={"input": "world"})

    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\n"
