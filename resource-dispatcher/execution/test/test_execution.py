import pytest
from importlib.util import find_spec
import execution


def test_all_plugins_loadable():
    plugins = ["ansible", "git", "kubernetes", "script"]
    for plugin in plugins:
        assert find_spec(f"execution.plugins.{plugin}") is not None
