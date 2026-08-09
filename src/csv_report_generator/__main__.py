import sys
from pathlib import Path

from csv_report_generator.cli import create_parser
from csv_report_generator.exceptions import CSVReportGeneratorError
from csv_report_generator.presenters import TablePresenter
from csv_report_generator.readers.csv_reader import CSVReader
from csv_report_generator.registry import ReportRegistry
from csv_report_generator.reports.performance import PerformanceReport
from csv_report_generator.services import ReportService


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()

    file_paths = [Path(file_path) for file_path in args.files]

    registry = ReportRegistry()
    registry.register(PerformanceReport())

    reader = CSVReader()
    service = ReportService(
        reader=reader,
        registry=registry,
    )
    presenter = TablePresenter()

    try:
        result = service.generate(
            file_paths=file_paths,
            report_name=args.report,
        )
        output = presenter.present(result)

    except CSVReportGeneratorError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())