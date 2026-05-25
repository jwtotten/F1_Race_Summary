# Adding a New Metric

## Steps

### 1. Create the collector file

Create `f1_race_summary/collectors/my_metric.py`. It is picked up automatically — no imports to add elsewhere.

```python
from . import register
from .base import BaseCollector, MetricResult
from ..session_loader import RaceSession

@register
class MyMetricCollector(BaseCollector):
    name = "my_metric"

    def collect(self, session: RaceSession) -> MetricResult:
        result = ...  # your logic here
        return MetricResult(name=self.name, data=result)
```

**Available data:**

| Attribute | What it gives you |
|-----------|------------------|
| `session.laps` | Per-lap DataFrame — `Driver`, `LapNumber`, `LapTime`, `Stint`, `Compound`, `TyreLife`, `Position` |
| `session.results` | Final standings — `Position`, `GridPosition`, `Abbreviation`, `Team`, `Points`, `Status` |
| `session.raw` | Full fastf1 `Session` object — use for `pos_data`, `car_data`, telemetry, etc. |
| `session.drivers` | List of driver identifiers in the session |

### 2. Add a field to `RaceReport`

In `f1_race_summary/report.py`:

```python
my_metric: SomeType | None = None
```

### 3. Wire it in `runner.py`

Add a branch to the `if/elif` block in `f1_race_summary/runner.py`:

```python
elif result.name == "my_metric":
    report.my_metric = result.data
```

### 4. Use it

`report.my_metric` is now available after `run(session)` returns in `main.py`.

---

## Notes

- If `collect()` raises `NotImplementedError` or any exception, `runner.py` catches it, stores the error in `report.errors["my_metric"]`, and continues — other metrics still run.
- `MetricResult.data` can be any type: `pd.DataFrame`, `dict`, `matplotlib.figure.Figure`, etc.
- See `position_chart.py` for a real matplotlib Figure example.
- See `top10.py` for the most detailed commented walkthrough of the pattern.
