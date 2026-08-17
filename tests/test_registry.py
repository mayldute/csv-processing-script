import pytest

from csv_report_generator.exceptions import DuplicateReportError, UnknownReportError
from csv_report_generator.registry import ReportRegistry
from csv_report_generator.reports.performance import PerformanceReport


def test_register_and_get_report():
    registry = ReportRegistry()
    report = PerformanceReport()

    registry.register(report)

    result = registry.get_report(report.name)

    assert result is report


def test_register_duplicate_report():
    registry = ReportRegistry()
    report = PerformanceReport()

    registry.register(report)

    with pytest.raises(DuplicateReportError) as exc_info:
        registry.register(report)

    assert report.name in str(exc_info.value)


def test_get_unknown_report():
    registry = ReportRegistry()

    with pytest.raises(UnknownReportError) as exc_info:
        registry.get_report("unknown_report")

    assert "unknown_report" in str(exc_info.value)
