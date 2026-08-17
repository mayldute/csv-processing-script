from decimal import Decimal

import pytest

from csv_report_generator.presenters import TablePresenter
from csv_report_generator.reports.performance import PerformanceReportRow


def test_present_dataclass_rows():
    rows = [
        PerformanceReportRow(
            position="QA",
            average_performance=Decimal("70.00"),
        ),
        PerformanceReportRow(
            position="Developer",
            average_performance=Decimal("85.00"),
        ),
    ]

    presenter = TablePresenter()

    result = presenter.present(rows)

    assert "position" in result
    assert "average_performance" in result
    assert "QA" in result
    assert "Developer" in result
    assert "70" in result
    assert "85" in result


def test_present_empty_rows():
    presenter = TablePresenter()

    result = presenter.present([])

    assert result == "No data available."


def test_present_non_dataclass_rows():
    rows = ["not a dataclass"]

    presenter = TablePresenter()

    with pytest.raises(TypeError) as exc_info:
        presenter.present(rows)

    assert str(exc_info.value) == "Table rows must be dataclass instances."
