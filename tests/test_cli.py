import pytest

from csv_report_generator.cli import create_parser


def test_parse_cli_arguments():
    parser = create_parser()

    args = parser.parse_args(
        [
            "--files",
            "first.csv",
            "second.csv",
            "--report",
            "performance",
        ]
    )

    assert args.files == ["first.csv", "second.csv"]
    assert args.report == "performance"


def test_parser_no_argument():
    parser = create_parser()

    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_parser_missing_files():
    parser = create_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["--report", "performance"])


def test_parser_missing_report():
    parser = create_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["--files", "employees.csv"])
