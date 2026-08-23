# Position-vs-lap chart collector.
# Build a matplotlib Figure showing each driver's position on every lap.
#
# Useful columns on session.laps:
#   Driver, LapNumber, Position
#
# data should be a matplotlib Figure — runner.py stores it as report.position_chart.
#
# Example:
#   import matplotlib.pyplot as plt
#
#   def collect(self, session: RaceSession) -> MetricResult:
#       fig, ax = plt.subplots(figsize=(12, 6))
#       for driver in session.laps["Driver"].unique():
#           driver_laps = session.laps[session.laps["Driver"] == driver]
#           ax.plot(driver_laps["LapNumber"], driver_laps["Position"], label=driver)
#       ax.invert_yaxis()   # position 1 at top
#       ax.set_xlabel("Lap")
#       ax.set_ylabel("Position")
#       ax.legend(fontsize=6, ncol=4)
#       return MetricResult(name=self.name, data=fig)

from . import register
from .base import BaseCollector, MetricResult
from ..session_loader import RaceSession

import matplotlib.pyplot as plt
import fastf1.plotting 


@register
class PositionChartCollector(BaseCollector):
    name = "position_chart"

    def collect(self, session: RaceSession) -> MetricResult:

        fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

        fig, ax = plt.subplots(figsize=(8, 4.9))
        for driver in session.raw.drivers:

            # Collecting the lap data for each driver
            driver_laps = session.laps.pick_driver(driver)
            driver_abbr = driver_laps["Driver"].iloc[0]
            driver_style = fastf1.plotting.get_driver_style(identifier=driver_abbr, style=['color', 'linestyle'], session=session.raw)

            # Plotting the lap data for each driver
            ax.plot(driver_laps["LapNumber"], driver_laps["Position"], label=driver_abbr, **driver_style)

        ax.set_ylim([20.5, 0.5])
        ax.set_yticks([1, 5, 10, 15, 20])
        ax.set_xlabel('Lap')
        ax.set_ylabel('Position')

        ax.legend(bbox_to_anchor=(1.0, 1.02))
        plt.tight_layout()

        return MetricResult(name=self.name, data=fig)
