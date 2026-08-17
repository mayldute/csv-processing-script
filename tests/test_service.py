import pytest
from pathlib import Path

from csv_report_generator.services import ReportService
from csv_report_generator.exceptions import (
    CSVFileNotFoundError, 
    UnknownReportError,
)


def test_generate_report(mocker):
    reader = mocker.Mock()
    registry = mocker.Mock()
    report = mocker.Mock()

    file_paths = [Path("employees.csv")]
    records = ["record"]
    expected_result = ["result"]

    reader.read.return_value = records
    registry.get_report.return_value = report
    report.generate.return_value = expected_result

    service = ReportService(
        reader=reader,
        registry=registry,
    )

    result = service.generate(
        file_paths=file_paths,
        report_name="performance",
    )

    assert result == expected_result
    reader.read.assert_called_once_with(file_paths)
    registry.get_report.assert_called_once_with("performance")
    report.generate.assert_called_once_with(records)


def test_generate_report_file_not_found(mocker):
    reader = mocker.Mock()
    registry = mocker.Mock()

    file_paths = [Path("non_existent_file.csv")]

    reader.read.side_effect = CSVFileNotFoundError("File not found")

    service = ReportService(
        reader=reader,
        registry=registry,
    )

    with pytest.raises(CSVFileNotFoundError) as exc_info:
        service.generate(
            file_paths=file_paths,
            report_name="performance",
        )

    assert "File not found" in str(exc_info.value)
    registry.get_report.assert_not_called()

def test_generate_report_unknown_report(mocker):
    reader = mocker.Mock()
    registry = mocker.Mock()
    report = mocker.Mock()

    file_paths = [Path("employees.csv")]
    records = ["record"]

    reader.read.return_value = records
    registry.get_report.side_effect = UnknownReportError(
        report_name="unknown_report",
        available_reports=("performance",),
    )

    service = ReportService(
        reader=reader,
        registry=registry,
    )

    with pytest.raises(UnknownReportError) as exc_info:
        service.generate(
            file_paths=file_paths,
            report_name="unknown_report",
        )

    assert "unknown_report" in str(exc_info.value)
    assert "performance" in str(exc_info.value)

    registry.get_report.assert_called_once_with("unknown_report")
    report.generate.assert_not_called()