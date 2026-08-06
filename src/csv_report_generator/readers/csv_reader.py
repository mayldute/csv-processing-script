import csv
from collections.abc import Sequence
from pathlib import Path

from csv_report_generator.exceptions import (
    CSVFileNotFoundError,
    InvalidCSVFileError,
)
from csv_report_generator.models import CSVRecord
from csv_report_generator.readers.base import DataReader


class CSVReader(DataReader):
    """Read records from CSV files."""

    def read(self, file_paths: Sequence[Path]) -> list[CSVRecord]:
        records: list[CSVRecord] = []

        for path in file_paths:
            if not path.exists():
                raise CSVFileNotFoundError(str(path))

            if not path.is_file():
                raise InvalidCSVFileError(
                    str(path),
                    "Path is not a file.",
                )

            if path.suffix.lower() != ".csv":
                raise InvalidCSVFileError(
                    str(path),
                    "File must have a .csv extension.",
                )

            with path.open(
                mode="r",
                encoding="utf-8-sig",
                newline="",
            ) as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    raise InvalidCSVFileError(
                        str(path),
                        "CSV header is missing.",
                    )

                for line_number, row in enumerate(reader, start=2):
                    values = {
                        key.strip(): (value or "").strip()
                        for key, value in row.items()
                        if key is not None
                    }

                    if not any(values.values()):
                        continue  # Skip empty rows

                    records.append(
                        CSVRecord(
                            values=values,
                            source=path,
                            line_number=line_number,
                        )
                    )

        return records