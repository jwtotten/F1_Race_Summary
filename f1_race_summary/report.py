from dataclasses import dataclass, field

import pandas as pd
from matplotlib.figure import Figure


@dataclass
class RaceReport:
    race_name: str
    session_date: str
    top10: pd.DataFrame | None = None           # from Top10Collector
    tyre_stints: pd.DataFrame | None = None     # from TyreCollector
    positions_delta: pd.DataFrame | None = None # from PositionsDeltaCollector
    overtake_count: int | None = None           # from OvertakeCollector
    overtake_detail: list[str] = field(default_factory=list)
    position_chart: Figure | None = None        # from PositionChartCollector
    errors: dict[str, list[str]] = field(default_factory=dict)
