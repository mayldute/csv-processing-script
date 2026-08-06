import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate analytical reports from CSV files.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        metavar="FILE",
        help="Paths to one or more CSV files.",
    )
    parser.add_argument(
        "--report",
        required=True,
        metavar="REPORT",
        help="Name of the report to generate.",
    )
    return parser