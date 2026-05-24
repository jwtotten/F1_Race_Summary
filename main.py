from f1_race_summary.config import load_config
from f1_race_summary.session_loader import load_session
from f1_race_summary.runner import run


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


if __name__ == "__main__":
    main()
