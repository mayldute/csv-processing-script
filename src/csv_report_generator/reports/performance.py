from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from csv_report_generator.reports.base import Report
from csv_report_generator.models import CSVRecord
from csv_report_generator.exceptions import InvalidRowError


@dataclass(frozen=True, slots=True)
class PerformanceReportRow:
    position: str
    average_performance: Decimal


class PerformanceReport(Report[PerformanceReportRow]):
    @property
    def name(self) -> str:
        return "performance"

    def generate(self, records: list[CSVRecord]) -> list[PerformanceReportRow]:
        performance_data: dict[str, list[Decimal]] = {}

        for record in records:
            position = record.values.get("position")
            performance_value = record.values.get("performance")

            if not position or not performance_value:
                raise InvalidRowError(
                    path=str(record.source),
                    line_number=record.line_number,
                    reason="missing 'position' or 'performance' value",
                )

            try:
                performance = Decimal(performance_value)
            except InvalidOperation as exc:
                raise InvalidRowError(
                    path=str(record.source),
                    line_number=record.line_number,
                    reason=f"invalid performance value: {performance_value!r}",
                ) from exc

            if position not in performance_data:
                performance_data[position] = []

            performance_data[position].append(performance)

        report_rows: list[PerformanceReportRow] = []

        for position, performances in performance_data.items():
            average_performance = round(
                sum(performances) / len(performances), 
                2,
            )
            report_rows.append(PerformanceReportRow(position, average_performance))

        return sorted(
            report_rows, 
            key=lambda row: row.average_performance,
        )