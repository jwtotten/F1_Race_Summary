# Tyre strategy collector.
# Return a DataFrame showing each driver's stints: compounds used and lap counts.
#
# Useful columns on session.laps:
#   Driver, Stint, Compound, TyreLife, LapNumber, FreshTyre
#
# Example shape of data to return:
#   DataFrame with columns: Driver, Stint, Compound, Laps
#
# Example:
#   def collect(self, session: RaceSession) -> MetricResult:
#       df = (
#           session.laps
#           .groupby(["Driver", "Stint", "Compound"])
#           .agg(Laps=("LapNumber", "count"))
#           .reset_index()
#       )
#       return MetricResult(name=self.name, data=df)

from . import register
from .base import BaseCollector, MetricResult
from ..session_loader import RaceSession


@register
class TyreCollector(BaseCollector):
    name = "tyres"

    def collect(self, session: RaceSession) -> MetricResult:
        raise NotImplementedError
