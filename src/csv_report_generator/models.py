from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CSVRecord:
    values: dict[str, str]
    source: Path
    line_number: int