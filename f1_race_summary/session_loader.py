from dataclasses import dataclass
from typing import Any

import fastf1
import pandas as pd

from .config import RaceConfig


@dataclass
class RaceSession:
    raw: fastf1.core.Session   # full fastf1 object — use for pos_data, car_data, etc.
    laps: pd.DataFrame         # session.laps shortcut
    results: pd.DataFrame      # session.results shortcut
    meta: dict[str, Any]       # year, gp, session string


def load_session(cfg: RaceConfig) -> RaceSession:
    fastf1.Cache.enable_cache(cfg.cache_dir)
    session = fastf1.get_session(cfg.year, cfg.gp, cfg.session)
    session.load()
    return RaceSession(
        raw=session,
        laps=session.laps,
        results=session.results,
        meta={"year": cfg.year, "gp": cfg.gp, "session": cfg.session},
    )
