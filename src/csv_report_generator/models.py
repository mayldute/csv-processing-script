from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CSVRecord:
    values: dict[str, str]
    source: Path
    line_number: int


@dataclass(frozen=True, slots=True)
class ReportResult:
    records: list[CSVRecord]
    report_name: str
