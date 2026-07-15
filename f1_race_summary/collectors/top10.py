# WORKED EXAMPLE — read this first before writing your own collectors.
#
# Pattern:
#   1. Import `register` and `BaseCollector` / `MetricResult` from this package.
#   2. Decorate your class with @register — this adds it to the auto-discovery list.
#   3. Set `name` to a snake_case string that matches the branch in runner.py.
#   4. Implement `collect(session)` — use session.laps, session.results, or
#      session.raw for anything needing the full fastf1 Session object.
#   5. Return MetricResult(name=self.name, data=<your payload>).
#      `data` can be a DataFrame, dict, Figure, or any other type — runner.py
#      maps it to the correct typed field on RaceReport.
#
# Example of a complete implementation (uncomment and fill in):
#
#   from . import register
#   from .base import BaseCollector, MetricResult
#   from ..session_loader import RaceSession
#
#   @register
#   class Top10Collector(BaseCollector):
#       name = "top10"
#
#       def collect(self, session: RaceSession) -> MetricResult:
#           df = session.results[["Position", "Abbreviation", "TeamName", "Time"]].head(10)
#           return MetricResult(name=self.name, data=df)
#
# session.results columns:
#   Position, GridPosition, Abbreviation, FullName, TeamName, Points, Status, Time

from . import register
from .base import BaseCollector, MetricResult
from ..session_loader import RaceSession

import matplotlib.pyplot as plt
import fastf1.plotting 


@register
class Top10Collector(BaseCollector):
    name = "top10"

    def collect(self, session: RaceSession) -> MetricResult:
        fastf1.plotting.setup_mpl(mpl_timedelta_support=False, color_scheme='fastf1')

        df = session.results[["Position", "Abbreviation", "TeamName", "Time"]].head(10)

        fig, ax = plt.subplots(figsize=(8, 4.9))
        ax.axis('off')

        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            cellLoc='center',
            loc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(15)
        table.auto_set_column_width(col=list(range(len(df.columns))))
        
        plt.tight_layout()

        return MetricResult(name=self.name, data=fig)
