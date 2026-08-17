from abc import ABC, abstractmethod
from collections.abc import Sequence

from csv_report_generator.models import CSVRecord


class Report[TResult](ABC):
    """Base class for reports."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the report name."""
        ...

    @abstractmethod
    def generate(self, records: list[CSVRecord]) -> Sequence[TResult]:
        """Generate the report based on the provided data."""
        ...
