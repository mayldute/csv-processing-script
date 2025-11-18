import argparse

def get_parser():
    parser = argparse.ArgumentParser(description="CSV report generator")
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--report", required=True)
    return parser
