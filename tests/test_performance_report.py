import pytest
from pathlib import Path

from csv_report_generator.models import CSVRecord
from csv_report_generator.reports.performance import PerformanceReport
from csv_report_generator.exceptions import InvalidRowError


def test_generate_performance_report():
    records = [
        CSVRecord(
            values={"position": "Developer", "performance": "90"},
            source=Path("employees.csv"),
            line_number=2,
        ),
        CSVRecord(
            values={"position": "Developer", "performance": "80"},
            source=Path("employees.csv"),
            line_number=3,
        ),
        CSVRecord(
            values={"position": "QA", "performance": "70"},
            source=Path("employees.csv"),
            line_number=4,
        ),
    ]

    report = PerformanceReport()

    result = report.generate(records)

    assert len(result) == 2
    assert result[0].position == "QA"
    assert result[0].average_performance == 70
    assert result[1].position == "Developer"
    assert result[1].average_performance == 85


def test_generate_missing_position():
    records = [
        CSVRecord(
            values={"position": "", "performance": "90"},
            source=Path("employees.csv"),
            line_number=2,
        ),
    ]

    report = PerformanceReport()

    with pytest.raises(InvalidRowError) as exc_info:
        report.generate(records)

    assert "position" in str(exc_info.value)
    assert str(records[0].line_number) in str(exc_info.value)


def test_generate_missing_performance():
    records = [
        CSVRecord(
            values={"position": "Developer", "performance": ""},
            source=Path("employees.csv"),
            line_number=2,
        ),
    ]

    report = PerformanceReport()

    with pytest.raises(InvalidRowError) as exc_info:
        report.generate(records)

    assert "performance" in str(exc_info.value)
    assert str(records[0].line_number) in str(exc_info.value)


def test_generate_invalid_performance():
    records = [
        CSVRecord(
            values={"position": "Developer", "performance": "abc"},
            source=Path("employees.csv"),
            line_number=2,
        ),
    ]

    report = PerformanceReport()

    with pytest.raises(InvalidRowError) as exc_info:
        report.generate(records)

    assert "abc" in str(exc_info.value)
    assert str(records[0].line_number) in str(exc_info.value)
