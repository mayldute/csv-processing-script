from csv_report_generator.exceptions import UnknownReportError, DuplicateReportError
from csv_report_generator.reports.base import Report


class ReportRegistry:
    def __init__(self) -> None:
        self._reports: dict[str, Report] = {}

    def register(self, report: Report) -> None:
        if report.name in self._reports:
            raise DuplicateReportError(report_name=report.name)

        self._reports[report.name] = report

    def get_report(self, report_name: str):
        report = self._reports.get(report_name)

        if report is None:
            raise UnknownReportError(
                report_name=report_name,
                available_reports=tuple(self._reports),
            )

        return report
