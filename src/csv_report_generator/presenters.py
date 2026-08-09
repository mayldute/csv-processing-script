from collections.abc import Sequence
from dataclasses import asdict, is_dataclass

from tabulate import tabulate


class TablePresenter:
    def present(self, rows: Sequence[object]) -> str:
        if not rows:
            return "No data available."

        if not all(is_dataclass(row) for row in rows):
            raise TypeError("Table rows must be dataclass instances.")

        table_data = [asdict(row) for row in rows]

        return tabulate(
            table_data,
            headers="keys",
            tablefmt="grid",
        )