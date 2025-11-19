import pytest

from csv_reports.performance import performance_report
from csv_reports.reports import generate_report


def test_generate_report_valid():
    rows = [
        {"position": "dev", "performance": "10"},
        {"position": "dev", "performance": "20"},
    ]

    result = generate_report("performance", rows)

    assert result == performance_report(rows)


def test_generate_report_invalid_name():
    with pytest.raises(ValueError) as exc:
        generate_report("unknown", [])

    assert "Unknown report" in str(exc.value)


def test_generate_report_calls_correct_function(mocker):
    mock_func = mocker.MagicMock(return_value="OK")

    mocker.patch.dict("csv_reports.reports.REPORTS", {"performance": mock_func})

    result = generate_report("performance", [])

    assert result == "OK"
    mock_func.assert_called_once_with([])


