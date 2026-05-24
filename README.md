# 🏎️ F1 Race Summary

> *"To finish first, first you must finish."* — Niki Lauda

Automated post-race stats summaries for F1 weekends. Pulls timing, tyre, and position data from [fastf1](https://docs.fastf1.dev/) and assembles a structured report you can slice any way you like.

---

## 📊 Current Metrics

> Did you know? The fastest recorded pit stop in F1 history is **1.80 seconds** — Red Bull Racing at the 2023 São Paulo Grand Prix. This tool won't make your pit stops faster, but it will tell you everyone else's tyre strategy.

| Metric | Description | Status |
|--------|-------------|--------|
| 🏁 Top 10 | Finishing positions, teams, and gaps for the top 10 | 🚧 stub |
| 🟡 Tyre Strategy | Compounds and stint lengths per driver | 🚧 stub |
| 💨 Overtakes | Total overtake count + detail per event | 🚧 stub |
| 📈 Position Chart | matplotlib figure — driver position vs lap number | 🔄 in progress |
| ⬆️ Positions Delta | Positions gained or lost from grid to finish | 🚧 stub |

---

## 🚀 Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
# Install dependencies and create virtual environment
uv sync
```

---

## 🔧 Usage

```bash
uv run python main.py --year 2024 --gp Monaco --session R
```

| Argument | Description | Example |
|----------|-------------|---------|
| `--year` | Season year | `2024` |
| `--gp` | Grand Prix name | `Monaco`, `Silverstone`, `Monza` |
| `--session` | Session type | `R` (race), `Q` (quali), `FP1`, `FP2`, `FP3` |

> *F1 has 20 rounds per season across 5 continents. This tool covers all of them — as long as fastf1 has the data.*

---

## 🤝 Contributing — Adding a New Metric

> *"The details are not the details. They make the design."* — not an F1 quote, but it applies.

The collector system is plug-and-play. Adding a new metric touches 3 files and takes about 5 minutes.

**Quick version:**

1. Create `f1_race_summary/collectors/my_metric.py` with a `@register` class
2. Add a field to `RaceReport` in `f1_race_summary/report.py`
3. Wire it in `f1_race_summary/runner.py`
4. Access it via `report.my_metric` in `main.py`

See [ADDING_A_METRIC.md](./ADDING_A_METRIC.md) for the full walkthrough with code examples.

---

## 🗂️ Project Structure

```
f1_race_summary/
├── main.py                        # entry point
├── f1_race_summary/
│   ├── config.py                  # CLI args → RaceConfig
│   ├── session_loader.py          # fastf1 wrapper → RaceSession
│   ├── runner.py                  # runs collectors → RaceReport
│   ├── report.py                  # RaceReport dataclass
│   └── collectors/
│       ├── base.py                # BaseCollector + MetricResult
│       ├── top10.py
│       ├── tyres.py
│       ├── overtakes.py
│       ├── position_chart.py
│       └── positions_delta.py
└── cache/                         # fastf1 local cache (gitignored)
```

Full architecture details: [ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 📦 Dependencies

- [fastf1](https://docs.fastf1.dev/) — F1 timing and telemetry data
- [pandas](https://pandas.pydata.org/) — data wrangling
- [matplotlib](https://matplotlib.org/) — charting
- [uv](https://docs.astral.sh/uv/) — package management

---

*Built with 🏎️ and too much race-day caffeine.*
