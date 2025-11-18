from cli.parser import get_parser
from csv_reports.reader import read_csv_files
from csv_reports.reports import generate_report
from tabulate import tabulate

def main():
    parser = get_parser()
    args = parser.parse_args()

    rows = read_csv_files(args.files)
    result = generate_report(args.report, rows)

    print(tabulate(result, headers="keys", tablefmt="grid"))

if __name__ == "__main__":
    main()
