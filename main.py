from f1_race_summary.config import load_config
from f1_race_summary.session_loader import load_session
from f1_race_summary.runner import run

from dataclasses import fields
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def main() -> None:
    cfg = load_config()
    session = load_session(cfg)
    report = run(session)

    print(f"\n=== {report.race_name} ===")
    print(f"Top 10:          {'ready' if report.top10 is not None else 'not implemented'}")
    print(f"Tyre stints:     {'ready' if report.tyre_stints is not None else 'not implemented'}")
    print(f"Positions delta: {'ready' if report.positions_delta is not None else 'not implemented'}")
    print(f"Overtakes:       {'ready' if report.overtake_count is not None else 'not implemented'}")
    print(f"Position chart:  {'ready' if report.position_chart is not None else 'not implemented'}")

    if report.errors:
        print("\nErrors:")
        for name, errs in report.errors.items():
            for e in errs:
                print(f"  {name}: {e}")

    if cfg.generate_report:
        for f in fields(report):
            value = getattr(report, f.name)
            print(f"\n--- {f.name} ---")
            print(f"Type: {type(value)}")
            if value is None:
                continue
            SKIP = {"race_name", 
                    "session_date", 
                    "errors", 
                    "overtake_detail",
                    "errors"}
            if f.name in SKIP:
                continue
            # dispatch by type
            if isinstance(value, Figure):
                plt.figure(value.number)
                plt.show()
            elif isinstance(value, pd.DataFrame):
                print(f.name, value)


if __name__ == "__main__":
    main()
