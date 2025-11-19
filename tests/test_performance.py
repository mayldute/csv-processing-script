from csv_reports.performance import performance_report


def test_basic_case():
    rows = [
        {"position": "dev", "performance": "10"},
        {"position": "dev", "performance": "20"},
        {"position": "qa", "performance": "30"},
    ]

    result = performance_report(rows)

    assert result == [
        {"position": "dev", "performance": 15.0},
        {"position": "qa", "performance": 30.0},
    ]


def test_sorted_output():
    rows = [
        {"position": "manager", "performance": "50"},
        {"position": "dev", "performance": "10"},
        {"position": "dev", "performance": "20"},
    ]

    result = performance_report(rows)

    # dev avg = 15; manager = 50
    assert result == [
        {"position": "dev", "performance": 15.0},
        {"position": "manager", "performance": 50.0},
    ]


def test_single_position():
    rows = [
        {"position": "designer", "performance": "40"},
        {"position": "designer", "performance": "60"},
    ]

    result = performance_report(rows)

    assert result == [
        {"position": "designer", "performance": 50.0}
    ]


def test_empty_input():
    assert performance_report([]) == []


def test_performance_as_string():
    rows = [
        {"position": "dev", "performance": "7.89"},
        {"position": "dev", "performance": "7.91"},
    ]

    result = performance_report(rows)

    # (7.89 + 7.91) / 2 = 7.90
    assert result == [{"position": "dev", "performance": 7.9}]
