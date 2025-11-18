# CSV Report Generator

This project provides a command-line tool for generating analytical reports based on CSV files containing task performance data. It supports multiple input files and is designed with extendability in mind, allowing new reports to be added easily.

## Features

* Read and combine multiple CSV files
* Generate reports (currently: **performance**)
* Output results as formatted tables
* Clean and modular architecture for adding new report types

## Usage

```bash
python3 main.py --files file1.csv file2.csv --report performance
```

## CSV Format

Each file must contain the following columns:

```
position, performance
```

Example:

```
Backend Developer,4.8
QA Engineer,4.5
```

## Adding a New Report

1. Create a new report function inside `csv_reports/`.
2. Register it in `csv_reports/reports.py` inside the `REPORTS` dictionary.
3. Run the tool using `--report <report_name>`.

## Tests

Unit tests are located in the `tests/` directory and can be run with:

```bash
pytest --cov
```
