from .collectors import get_collectors
from .report import RaceReport
from .session_loader import RaceSession


def run(session: RaceSession) -> RaceReport:
    report = RaceReport(
        race_name=f"{session.meta['year']} {session.meta['gp']}",
        session_date=str(session.raw.date.date()) if hasattr(session.raw, "date") else "",
    )

    for collector in get_collectors():
        try:
            result = collector.collect(session)
        except NotImplementedError:
            report.errors[collector.name] = ["not implemented yet"]
            continue
        except Exception as exc:
            report.errors[collector.name] = [str(exc)]
            continue

        # Map each result to its typed field on RaceReport.
        # Add a new branch here when you add a collector with a new report field.
        if result.name == "top10":
            report.top10 = result.data
        elif result.name == "tyres":
            report.tyre_stints = result.data
        elif result.name == "positions_delta":
            report.positions_delta = result.data
        elif result.name == "overtakes":
            report.overtake_count = result.data.get("count")
            report.overtake_detail = result.data.get("detail", [])
        elif result.name == "position_chart":
            report.position_chart = result.data

        if result.errors:
            report.errors.setdefault(result.name, []).extend(result.errors)

    return report
