def performance_report(rows):
    stats = {}

    for row in rows:
        pos = row["position"]
        perf = float(row["performance"])

        if pos not in stats:
            stats[pos] = {"sum": 0, "count": 0}

        stats[pos]["sum"] += perf
        stats[pos]["count"] += 1

    result = [
        {"position": pos, "performance": round(values["sum"] / values["count"], 2)}
        for pos, values in stats.items()
    ]

    return sorted(result, key=lambda x: x["performance"])
