# CSV Report Generator

[![CI](https://github.com/mayldute/csv-processing-script/actions/workflows/ci.yml/badge.svg)](https://github.com/mayldute/csv-processing-script/actions/workflows/ci.yml)

Production-oriented Python application for processing CSV datasets and generating analytical reports through an extensible report architecture.

## Features

- CSV file validation and parsing
- Support for multiple CSV input files
- Required column validation
- Empty row handling
- Structured CSV records with source file and line number
- Extensible report architecture
- Report registry with duplicate and unknown report validation
- Performance report with grouped averages and sorting
- Decimal-based calculations
- Custom exception hierarchy
- Human-readable table output with `tabulate`
- Command-line interface
- Type hints throughout the project
- Automated tests with `pytest`
- Test coverage reporting
- Code formatting and linting with Ruff

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Installation

Install the project together with development dependencies:

```bash
uv sync --extra dev
```

## Usage

Run the application through the command line:

```bash
uv run python -m csv_report_generator --files employees.csv --report performance
```

Multiple CSV files can be processed at once:

```bash
uv run python -m csv_report_generator --files employees_1.csv employees_2.csv --report performance
```

### CSV Format

The `performance` report expects the following columns:

```csv
position,performance
Developer,90
Developer,80
QA,70
```

The `CSVReader` validates the file, CSV header, and required columns before processing the data. Empty rows are ignored.

### Example Output

```text
+------------+---------------------+
| position   | average_performance |
+------------+---------------------+
| QA         | 70.00               |
| Developer  | 85.00               |
+------------+---------------------+
```

Reports are sorted by average performance in ascending order.

## Architecture

The application is split into small components with clear responsibilities:

```text
CLI
 │
 ▼
ReportService
 │
 ├── DataReader
 │      └── CSVReader
 │
 └── ReportRegistry
        └── Report
              └── PerformanceReport
 │
 ▼
TablePresenter
 │
 ▼
Console output
```

### Data Reader

`DataReader` defines the interface for reading input data.

`CSVReader` is responsible for:

- validating file paths;
- validating CSV extensions;
- validating CSV headers;
- validating required columns;
- reading CSV records;
- preserving source file and line number;
- ignoring empty rows.

### Reports

Reports implement the generic `Report[TResult]` abstraction. Each report defines its own result-row dataclass and generation logic.

For example:

```text
Report[PerformanceReportRow]
          │
          ▼
  PerformanceReport
```

This allows new report types to be added without changing the reader or service layers.

### Report Registry

`ReportRegistry` stores available reports and provides them by name.

It prevents duplicate registrations and raises an error when an unknown report is requested.

### Report Service

`ReportService` coordinates the main application flow:

```text
CSV files
   ↓
DataReader
   ↓
CSV records
   ↓
ReportRegistry
   ↓
Report
   ↓
Report result
```

The service receives its dependencies through dependency injection.

### Table Presenter

`TablePresenter` converts report-result dataclasses into human-readable tables using `tabulate`.

## Error Handling

The project uses a custom exception hierarchy:

```text
CSVReportGeneratorError
├── CSVReadError
├── CSVFileNotFoundError
├── InvalidCSVFileError
│   └── MissingColumnsError
├── InvalidRowError
├── UnknownReportError
└── DuplicateReportError
```

Expected application errors are handled by the CLI and displayed through `stderr` with a non-zero exit code.

## Testing

Run the complete test suite:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=csv_report_generator --cov-report=term-missing
```

The test suite covers:

- CSV reading and validation
- missing files
- invalid file types
- missing CSV headers
- missing required columns
- empty rows
- report generation and sorting
- invalid report data
- report registration
- duplicate and unknown reports
- service orchestration
- table presentation
- CLI argument parsing
- application entry point
- application error handling

## Code Quality

Format the project:

```bash
uv run ruff format .
```

Run linting:

```bash
uv run ruff check .
```

Automatically fix supported lint issues:

```bash
uv run ruff check . --fix
```
## Continuous Integration

The project uses GitHub Actions to automatically validate every push and pull request.

The CI pipeline:

- installs Python and project dependencies;
- runs Ruff linting;
- runs the complete pytest test suite.

A change is considered valid only when all CI checks pass.

The workflow is defined in `.github/workflows/ci.yml`.

## Adding a New Report

The report architecture is designed to make adding new report types straightforward.

### 1. Create a result row

Define a dataclass representing the report output:

```python
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class ExampleReportRow:
    category: str
    value: Decimal
```

### 2. Implement the report

Create a class inheriting from `Report`:

```python
class ExampleReport(Report[ExampleReportRow]):
    @property
    def name(self) -> str:
        return "example"

    def generate(
        self,
        records: list[CSVRecord],
    ) -> list[ExampleReportRow]: ...
```

### 3. Register the report

Register the new report with `ReportRegistry`:

```python
registry.register(ExampleReport())
```

The existing reader, service, presenter, and CLI architecture can then be reused without modification.

## Development Workflow

Before committing changes, run:

```bash
uv run pytest
uv run ruff format .
uv run ruff check .
```
```markdown
These checks are also executed automatically by GitHub Actions on every push and pull request.
```

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/mayldute/csv-processing-script/blob/main/LICENSE) file for details.
