from collections.abc import Sequence
from pathlib import Path

from csv_report_generator.readers.base import DataReader
from csv_report_generator.registry import ReportRegistry


class ReportService:
    def __init__(self, reader: DataReader, registry: ReportRegistry) -> None:
        self.reader = reader
        self.registry = registry

    def generate(
        self, file_paths: Sequence[Path], report_name: str
    ) -> Sequence[object]:
        records = self.reader.read(file_paths)
        report = self.registry.get_report(report_name)
        return report.generate(records)
