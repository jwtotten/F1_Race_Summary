# f1_race_summary — Architecture

## Overview

The app is a two-stage pipeline: a data layer loads and normalises race data from fastf1; a collector layer runs independent metric functions against that data and assembles results into a `RaceReport`. Collectors are registered via a decorator and auto-discovered at import time, so adding a new metric requires touching only one file. Output/rendering is handled separately (e.g. a matplotlib script) consuming the `RaceReport`.

---

## Directory Tree

```
f1_race_summary/
├── pyproject.toml                   # project metadata and dependencies
├── main.py                          # entry point — wires config → session → run
├── cache/                           # fastf1 disk cache (gitignored)
└── f1_race_summary/
    ├── __init__.py                  # package marker
    ├── config.py                    # RaceConfig dataclass + CLI loader
    ├── session_loader.py            # loads fastf1 session, returns RaceSession
    ├── runner.py                    # runs collectors, assembles RaceReport
    ├── report.py                    # RaceReport dataclass definition
    └── collectors/
        ├── __init__.py              # registry + auto-discovery of collector modules
        ├── base.py                  # BaseCollector ABC + MetricResult dataclass
        ├── tyres.py                 # TyreCollector (implement here)
        ├── top10.py                 # Top10Collector (implement here)
        ├── overtakes.py             # OvertakeCollector (implement here)
        ├── position_chart.py        # PositionChartCollector (implement here)
        └── positions_delta.py       # PositionsDeltaCollector (implement here)
```

---

## Interface Definitions

### `config.py`

```python
@dataclass
class RaceConfig:
    year: int
    gp: str
    session: str = "R"
    cache_dir: str = "./cache"

def load_config() -> RaceConfig: ...
# reads --year, --gp, --session from CLI via argparse
```

### `session_loader.py`

```python
@dataclass
class RaceSession:
    raw: fastf1.core.Session      # full fastf1 Session object for collectors that need it
    laps: pd.DataFrame            # session.laps — pre-loaded convenience reference
    results: pd.DataFrame         # session.results
    meta: dict[str, Any]          # year, gp, session identifier

def load_session(cfg: RaceConfig) -> RaceSession: ...
# enables fastf1 cache, calls get_session(), session.load(), returns RaceSession
```

### `collectors/base.py`

```python
@dataclass
class MetricResult:
    name: str
    data: Any                          # collector-specific payload, typed by each collector
    errors: list[str] = field(default_factory=list)

class BaseCollector(ABC):
    name: str                          # unique snake_case identifier, e.g. "tyres"

    @abstractmethod
    def collect(self, session: RaceSession) -> MetricResult: ...
```

### `collectors/__init__.py`

```python
_REGISTRY: list[type[BaseCollector]] = []

def register(cls: type[BaseCollector]) -> type[BaseCollector]: ...
def get_collectors() -> list[BaseCollector]: ...
# auto-discovers all *.py files in collectors/ via pkgutil at import time
```

### `report.py`

```python
@dataclass
class RaceReport:
    race_name: str
    session_date: str
    top10: pd.DataFrame               # Position, Driver, Team, Time/Gap
    tyre_stints: pd.DataFrame         # Driver, Stint, Compound, Laps
    positions_delta: pd.DataFrame     # Driver, StartPos, FinishPos, Delta
    overtake_count: int
    overtake_detail: list[str]        # one string per overtake event
    position_chart: Figure            # matplotlib Figure from PositionChartCollector
    errors: dict[str, list[str]]      # collector name → error list
```

### `runner.py`

```python
def run(session: RaceSession) -> RaceReport: ...
# calls get_collectors(), runs collect(session) on each,
# maps MetricResult.data by collector name into RaceReport fields
```

### `main.py` (wiring only)

```python
def main() -> None:
    cfg = load_config()
    session = load_session(cfg)
    report = run(session)
    # pass report to your output script / matplotlib visualisation
```

---

## How to Add a New Metric

1. Create `f1_race_summary/collectors/my_metric.py`.
2. Define a dataclass for the payload (e.g. `MyData`).
3. Write a class inheriting `BaseCollector` with `name = "my_metric"` and decorate it with `@register`.
4. Implement `collect(self, session: RaceSession) -> MetricResult` — return `MetricResult(name=self.name, data=<MyData instance>)`.
5. Add the corresponding typed field to `RaceReport` in `report.py` and update `runner.py` to pull `result.data` from the collector where `result.name == "my_metric"`.

No changes needed to any other file — the auto-discovery in `collectors/__init__.py` imports the new module automatically.

---

## Data Flow

`main.py` parses CLI args via `load_config()` to produce a `RaceConfig`, passes it to `load_session()` which calls fastf1, caches the session to disk, and returns a `RaceSession` containing both the raw fastf1 `Session` object and pre-extracted convenience DataFrames. `runner.run(session)` retrieves all registered collectors via `get_collectors()`, calls `collect(session)` on each in sequence, and maps the named `MetricResult` payloads into the fixed fields of a `RaceReport`. The `RaceReport` is then available for any output script or matplotlib visualisation to consume.

---

## Key Design Decisions

- **Collectors receive `RaceSession`, not the raw fastf1 `Session`.** `RaceSession` wraps `fastf1.core.Session` as `.raw` and exposes pre-extracted `laps` and `results` DataFrames. Collectors avoid duplicating boilerplate loading calls while retaining full fastf1 API access via `.raw` when needed.

- **Collector output is `MetricResult`; the pipeline assembles `RaceReport` in `runner.py`.** Collectors stay generic and testable in isolation. `runner.py` is the single place that knows the mapping from collector names to typed `RaceReport` fields. If a collector fails, its errors land in `RaceReport.errors` and the run continues.

- **`runner.py` owns assembly; `main.py` owns wiring only.** `main.py` is intentionally thin — parse config, load session, call `run()`. No business logic lives there. `runner.py` is independently testable without going through the CLI.

- **Auto-discovery via `pkgutil` in `collectors/__init__.py`.** Dropping a new `.py` file into `collectors/` is enough to get it imported and registered. The `@register` decorator opts the class in. No explicit import list to maintain.

- **`RaceReport` is a fixed-shape typed dataclass, not a generic dict.** Downstream output scripts get stable, named fields. A dict would push type errors to runtime; a dataclass surfaces them at the runner boundary where they are cheapest to catch.

---

## fastf1 Quick Reference

The key data available via `RaceSession`:

| Source | What it contains |
|--------|-----------------|
| `session.laps` | Per-lap data: `Driver`, `LapNumber`, `LapTime`, `Stint`, `Compound`, `TyreLife`, `Position` |
| `session.results` | Final standings: `Position`, `GridPosition`, `Abbreviation`, `Team`, `Points`, `Status` |
| `session.raw.pos_data` | Per-driver position tracking data (for position-vs-lap chart) |
| `session.raw.car_data` | High-frequency telemetry (Speed, Throttle, Brake, DRS, Gear) |

Load a session:
```python
import fastf1
fastf1.Cache.enable_cache("./cache")
session = fastf1.get_session(2024, "Monaco", "R")
session.load()
```
