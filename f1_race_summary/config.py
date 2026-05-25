from dataclasses import dataclass
import argparse


@dataclass
class RaceConfig:
    year: int
    gp: str
    session: str = "R"
    cache_dir: str = "./f1_race_summary/.cache"
    generate_report: bool = False


def load_config() -> RaceConfig:
    parser = argparse.ArgumentParser(description="F1 Race Summary")
    parser.add_argument("--year", type=int, required=True, help="Season year, e.g. 2024")
    parser.add_argument("--gp", type=str, required=True, help="Grand Prix name, e.g. Monaco")
    parser.add_argument("--session", type=str, default="R", help="Session type: R, Q, S, FP1, FP2, FP3")
    parser.add_argument("--cache-dir", type=str, default="./f1_race_summary/.cache", dest="cache_dir")
    parser.add_argument("--generate-report", action="store_true", help="Generate the report (default: False)", required=False)
    args = parser.parse_args()
    return RaceConfig(year=args.year, gp=args.gp, session=args.session, cache_dir=args.cache_dir, generate_report=args.generate_report)
