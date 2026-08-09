from abc import ABC, abstractmethod

from csv_report_generator.models import CSVRecord


class Report(ABC):
    """Base class for reports."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the report name."""
        ...

    @abstractmethod
    def generate(self, records: list[CSVRecord]):
        """Generate the report based on the provided data."""
        ...