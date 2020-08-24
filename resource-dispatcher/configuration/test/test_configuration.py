import pytest
import os
import configuration


def test_exits_without_configuration():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        configuration.get_config()
    assert pytest_wrapped_e.type == SystemExit


def test_get_config(monkeypatch):
    monkeypatch.setenv("CONFIG_FILE", os.getcwd() + "/configuration/test/config_exists.yml")
    config = configuration.get_config()
    assert {"hello": "world"} == config
