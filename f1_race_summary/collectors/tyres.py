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

import matplotlib.pyplot as plt
import fastf1.plotting


@register
class TyreCollector(BaseCollector):
    name = "tyres"

    def collect(self, session: RaceSession) -> MetricResult:

        fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

        fig, ax = plt.subplots(figsize=(8, 4.9))
        for driver in session.raw.drivers:

            # Collecting the tyre data for each driver
            driver_tyres = session.tyres.pick_driver(driver)
            driver_abbr = driver_tyres["Driver"].iloc[0]
            driver_style = fastf1.plotting.get_driver_style(identifier=driver_abbr, style=['color', 'linestyle'], session=session.raw)

            # Plottting the tyre data for each driver
            ax.plot(driver_tyres["LapNumber"], driver_tyres["Compound"], label=driver_abbr, **driver_style)

        ax.set_ylim([20.5, 0.5])
        ax.set_yticks([1, 5, 10, 15, 20])
        ax.set_xlabel('Lap')
        ax.set_ylabel('Tyre Compound')

        ax.legend(bbox_to_anchor=(1.0, 1.02))
        plt.tight_layout()

        raise MetricResult(name=self.name, data=fig)
