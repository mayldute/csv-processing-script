import pytest
from pathlib import Path

from csv_report_generator.readers.csv_reader import CSVReader
from csv_report_generator.exceptions import (
    CSVFileNotFoundError,
    InvalidCSVFileError,
)


def test_read_valid_csv(tmp_path: Path):
    csv_file = tmp_path / "employees.csv"
    csv_file.write_text(
        "position,performance\nDeveloper,90\nQA,80\n",
        encoding="utf-8",
    )

    reader = CSVReader()

    records = reader.read([csv_file])

    assert len(records) == 2
    assert records[0].values == {"position": "Developer", "performance": "90"}
    assert records[0].source == csv_file
    assert records[0].line_number == 2
    assert records[1].values == {"position": "QA", "performance": "80"}
    assert records[1].source == csv_file
    assert records[1].line_number == 3


def test_read_missing_csv_file(tmp_path: Path):
    missing_file = tmp_path / "missing.csv"

    reader = CSVReader()

    with pytest.raises(CSVFileNotFoundError) as exc_info:
        reader.read([missing_file])

    assert str(missing_file) in str(exc_info.value)


def test_read_file_with_wrong_extension(tmp_path: Path):
    wrong_file = tmp_path / "data.txt"
    wrong_file.write_text(
        "position,performance\nDeveloper,90\nQA,80\n",
        encoding="utf-8",
    )

    reader = CSVReader()

    with pytest.raises(InvalidCSVFileError) as exc_info:
        reader.read([wrong_file])

    assert str(wrong_file) in str(exc_info.value)


def test_read_csv_with_empty_rows(tmp_path: Path):
    csv_file = tmp_path / "employees.csv"
    csv_file.write_text(
        "position,performance\nDeveloper,90\n\nQA,80\n",
        encoding="utf-8",
    )

    reader = CSVReader()

    records = reader.read([csv_file])

    assert len(records) == 2
    assert records[0].values == {"position": "Developer", "performance": "90"}
    assert records[0].source == csv_file
    assert records[0].line_number == 2
    assert records[1].values == {"position": "QA", "performance": "80"}
    assert records[1].source == csv_file
    assert records[1].line_number == 3


def test_read_directory_instead_of_file(tmp_path: Path):
    directory = tmp_path / "employees.csv"
    directory.mkdir()

    reader = CSVReader()

    with pytest.raises(InvalidCSVFileError) as exc_info:
        reader.read([directory])

    assert str(directory) in str(exc_info.value)
