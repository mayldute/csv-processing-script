from unittest.mock import patch

from csv_report_generator.__main__ import main
from csv_report_generator.exceptions import CSVReportGeneratorError


def test_main_success(capsys):
    with patch(
        "csv_report_generator.__main__.ReportService.generate",
        return_value=[],
    ):
        with patch(
            "csv_report_generator.__main__.TablePresenter.present",
            return_value="Report output",
        ):
            with patch(
                "sys.argv",
                [
                    "csv-report-generator",
                    "--files",
                    "employees.csv",
                    "--report",
                    "performance",
                ],
            ):
                result = main()

    captured = capsys.readouterr()

    assert result == 0
    assert captured.out == "Report output\n"
    assert captured.err == ""


def test_main_handles_application_error(capsys):
    with patch(
        "csv_report_generator.__main__.ReportService.generate",
        side_effect=CSVReportGeneratorError("Something went wrong"),
    ):
        with patch(
            "sys.argv",
            [
                "csv-report-generator",
                "--files",
                "employees.csv",
                "--report",
                "performance",
            ],
        ):
            result = main()

    captured = capsys.readouterr()

    assert result == 1
    assert captured.out == ""
    assert "Error: Something went wrong" in captured.err
