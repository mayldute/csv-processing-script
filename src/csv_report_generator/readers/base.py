from abc import ABC, abstractmethod
from collections.abc import Sequence
from pathlib import Path

from csv_report_generator.models import CSVRecord


class DataReader(ABC):
    """Interface for data readers."""

    @abstractmethod
    def read(self, files: Sequence[Path]) -> list[CSVRecord]:
        """Read records from the specified files."""
        ...
