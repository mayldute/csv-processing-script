import tempfile
import os

from csv_reports.reader import read_csv_files


def test_read_single_csv():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write("position,performance\n")
        tmp.write("Backend Developer,4.8\n")
        tmp_path = tmp.name

    rows = read_csv_files([tmp_path])

    assert len(rows) == 1
    assert rows[0]["position"] == "Backend Developer"
    assert rows[0]["performance"] == "4.8"

    os.remove(tmp_path)


def test_read_multiple_csv_files():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode="w+", delete=False) as f2:

        f1.write("position,performance\nBackend,4.8\n")
        f2.write("position,performance\nQA,4.5\n")

        p1 = f1.name
        p2 = f2.name

    rows = read_csv_files([p1, p2])

    assert len(rows) == 2
    assert rows[0]["position"] == "Backend"
    assert rows[1]["position"] == "QA"

    os.remove(p1)
    os.remove(p2)


def test_empty_csv():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write("position,performance\n")
        path = tmp.name

    rows = read_csv_files([path])
    assert rows == []

    os.remove(path)


def test_file_not_found():
    fake_path = "no_such_file_123.csv"
    try:
        read_csv_files([fake_path])
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True
