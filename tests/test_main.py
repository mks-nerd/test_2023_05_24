from datetime import datetime
from main import read_file, parse_log, process_logs, generate_report, print_report


def test_read_file():
    path = "tests/data_test.txt"
    data = read_file(path=path)
    assert isinstance(data, list)
    assert isinstance(data[0], str)
    assert len(data) == 11

    fail = read_file(path="")
    assert fail is None


def test_parse_log():
    log = "14:02:03 ALICE99 Start\n"
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

    expected_data = {"ALICE99": [31.0, 92.0, 67.0, 50.0], "CHARLIE": [2.0, 35.0, 0.0]}

    assert isinstance(data, dict)
    assert data == expected_data

    fail = process_logs([])

    assert fail is None


def test_generate_report():
    path = "tests/data_test.txt"
    data = generate_report(path)
    expected_result = "ALICE99 4 240\nCHARLIE 3 37"

    assert isinstance(data, str)
    assert data == expected_result

    path = "tests/data_test"
    fail = generate_report(path)
    expected_failed_result = "Can't Read File"

    assert isinstance(fail, str)
    assert fail == expected_failed_result


def test_print_report():
    from subprocess import run

    result = run(
        ["python", "main.py", "tests/data_test.txt"], capture_output=True, text=True
    )
    result = result.stdout.strip()
    expected_result = "ALICE99 4 240\nCHARLIE 3 37"

    assert isinstance(result, str)
    assert result == expected_result

    result = run(["python", "main.py"], capture_output=True, text=True)
    fail = result.stdout.strip()
    expected_failed_result = "Usage: python main.py <file_path>"

    assert isinstance(fail, str)
    assert result == expected_failed_result

    result = run(["python", "main.py", "invalid_file"], capture_output=True, text=True)
    fail = result.stdout.strip()
    expected_failed_result = "Can't Read File"

    assert isinstance(fail, str)
    assert result == expected_failed_result
