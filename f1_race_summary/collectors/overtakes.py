# Overtake counter collector.
# Count position changes between consecutive laps across all drivers.
#
# Useful columns on session.laps:
#   Driver, LapNumber, Position
#
# runner.py expects data to be a dict:
#   {"count": int, "detail": list[str]}
#
# Example:
#   def collect(self, session: RaceSession) -> MetricResult:
#       laps = session.laps[["Driver", "LapNumber", "Position"]].dropna()
#       # compare position lap N vs lap N-1 per driver to detect overtakes
#       ...
#       return MetricResult(name=self.name, data={"count": n, "detail": ["VER overtook HAM on lap 14", ...]})

from . import register
from .base import BaseCollector, MetricResult
from ..session_loader import RaceSession


@register
class OvertakeCollector(BaseCollector):
    name = "overtakes"

    def collect(self, session: RaceSession) -> MetricResult:
        raise NotImplementedError
