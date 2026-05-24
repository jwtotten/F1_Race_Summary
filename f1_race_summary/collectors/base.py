from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetricResult:
    name: str
    data: Any                          # shape is defined by each collector
    errors: list[str] = field(default_factory=list)


class BaseCollector(ABC):
    name: str                          # must match the key used in runner.py

    @abstractmethod
    def collect(self, session) -> MetricResult: ...
