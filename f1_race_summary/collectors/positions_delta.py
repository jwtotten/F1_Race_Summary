# Positions gained/lost collector.
# Compare each driver's grid position to their finishing position.
#
# Useful columns on session.results:
#   Abbreviation, GridPosition, Position
#
# Example shape of data to return:
#   DataFrame with columns: Driver, StartPos, FinishPos, Delta
#   where Delta = GridPosition - Position (positive = gained places)
#
# Example:
#   def collect(self, session: RaceSession) -> MetricResult:
#       df = session.results[["Abbreviation", "GridPosition", "Position"]].copy()
#       df = df.rename(columns={"Abbreviation": "Driver", "GridPosition": "StartPos", "Position": "FinishPos"})
#       df["Delta"] = df["StartPos"] - df["FinishPos"]
#       return MetricResult(name=self.name, data=df.sort_values("Delta", ascending=False))

from . import register
from .base import BaseCollector, MetricResult
from ..session_loader import RaceSession


@register
class PositionsDeltaCollector(BaseCollector):
    name = "positions_delta"

    def collect(self, session: RaceSession) -> MetricResult:
        raise NotImplementedError
