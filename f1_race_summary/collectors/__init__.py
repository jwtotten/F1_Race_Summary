import importlib
import pathlib
import pkgutil

from .base import BaseCollector

_REGISTRY: list[type[BaseCollector]] = []


def register(cls: type[BaseCollector]) -> type[BaseCollector]:
    _REGISTRY.append(cls)
    return cls


def get_collectors() -> list[BaseCollector]:
    return [cls() for cls in _REGISTRY]


# Auto-discover every *.py file in this directory except base.py.
# Drop a new collector file here and it is picked up automatically.
for _mod in pkgutil.iter_modules([str(pathlib.Path(__file__).parent)]):
    if _mod.name != "base":
        importlib.import_module(f".{_mod.name}", package=__name__)
