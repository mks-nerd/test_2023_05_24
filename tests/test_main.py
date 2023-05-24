from subprocess import run
from datetime import datetime
from main import read_file, parse_log, process_logs


def test_read_file():
    path = "tests/data_test.txt"
    data = read_file(path=path)
    assert isinstance(data, list)
    assert isinstance(data[0], str)
    assert len(data) == 18

    fail = read_file(path="")
    assert fail is None


def test_parse_log():
    log: str = "14:02:03 ALICE99 Start\n"
    time, user, action = parse_log(log)

    assert isinstance(time, datetime)
    assert isinstance(user, str)
    assert isinstance(action, str)
    assert time == datetime.strptime("14:02:03", "%H:%M:%S")
    assert user == "ALICE99"
    assert action == "Start"

    fail = parse_log("xyz")

    assert fail is None


def test_process_logs():
    path = "tests/data_test.txt"
    data = read_file(path=path)
    data = process_logs(data)

    expected_data = {
        "ALICE99": {"session": 4, "total_time": 240},
        "CHARLIE": {"session": 3, "total_time": 37},
        "JJJJJJJ": {"session": 1, "total_time": 159},
        "sss4544": {"session": 1, "total_time": 0},
        "CH@RLI3": {"session": 1, "total_time": 0},
        "*******": {"session": 1, "total_time": 0},
    }

    assert isinstance(data, dict)
    assert data == expected_data
