from .performance import performance_report

REPORTS = {
    "performance": performance_report,
}

def generate_report(name, rows):
    if name not in REPORTS:
        raise ValueError(f"Unknown report: {name}")

    return REPORTS[name](rows)
