class CSVReportGeneratorError(Exception):
    """Base exception for the CSV report generator."""

    default_message = "An error occurred in the CSV report generator."

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class CSVReadError(CSVReportGeneratorError):
    """Exception raised for errors in reading CSV files."""

    default_message = "Failed to read the CSV file."


class CSVFileNotFoundError(CSVReadError):
    """Raised when a CSV file does not exist."""

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"CSV file was not found: {path}")


class InvalidCSVFileError(CSVReadError):
    """Raised when a CSV file has an invalid format."""

    def __init__(self, path: str, reason: str) -> None:
        self.path = path
        self.reason = reason
        super().__init__(f"Invalid CSV file '{path}': {reason}")


class MissingColumnsError(InvalidCSVFileError):
    """Raised when required columns are missing."""

    def __init__(
        self,
        path: str,
        missing_columns: set[str],
    ) -> None:
        self.missing_columns = missing_columns
        columns = ", ".join(sorted(missing_columns))

        super().__init__(
            path,
            f"missing required columns: {columns}",
        )


class InvalidRowError(InvalidCSVFileError):
    """Raised when a CSV row contains invalid data."""

    def __init__(
        self,
        path: str,
        line_number: int,
        reason: str,
    ) -> None:
        self.line_number = line_number

        super().__init__(
            path,
            f"invalid row at line {line_number}: {reason}",
        )


class UnknownReportError(CSVReportGeneratorError):
    """Raised when the requested report is not registered."""

    def __init__(
        self,
        report_name: str,
        available_reports: tuple[str, ...],
    ) -> None:
        self.report_name = report_name
        self.available_reports = available_reports

        available = ", ".join(available_reports) or "none"

        super().__init__(
            f"Unknown report '{report_name}'. Available reports: {available}."
        )


class DuplicateReportError(CSVReportGeneratorError):
    """Raised when a report name is registered more than once."""

    def __init__(self, report_name: str) -> None:
        self.report_name = report_name

        super().__init__(f"Report '{report_name}' is already registered.")
