import os
import sys
from datetime import datetime

import pytest

from main import (
    calculate_log_time,
    create_bin,
    generate_report,
    make_equal_bin_size,
    parse_all_logs,
    parse_log,
    print_report,
    process_logs,
    read_file,
    validate_username,
)


def test_read_file_existing_file():
    path = "test_data.txt"
    expected_result = [
        "14:02:03 ALICE99 Start\n",
        "14:02:05 CHARLIE End\n",
        "14:02:34 ALICE99 End\n",
        "14:02:58 ALICE99 Start\n",
        "14:03:02 CHARLIE Start\n",
        "14:03:33 ALICE99 Start\n",
        "14:03:35 ALICE99 End\n",
        "14:03:37 CHARLIE End\n",
        "14:04:05 ALICE99 End\n",
        "14:04:23 ALICE99 End\n",
        "14:04:41 CHARLIE Start",
    ]

    result = read_file(path)

    assert result == expected_result


def test_read_file_non_existing_file():
    path = "non_existing_file.txt"

    result = read_file(path)

    assert result is None


def test_read_file_empty_file():
    path = "empty_file.txt"

    with open(path, "w") as _:
        pass

    result = read_file(path)

    assert result is None

    os.remove(path)


def test_validate_username_valid():
    username = "Alice99"

    result = validate_username(username)

    assert result is True


def test_validate_username_invalid_start_with_number():
    username = "9Alice"

    result = validate_username(username)

    assert result is False


def test_validate_username_invalid_special_characters():
    username = "Alice#99"

    result = validate_username(username)

    assert result is False


def test_validate_username_invalid_whitespace():
    username = "Alice 99"

    result = validate_username(username)

    assert result is False


def test_validate_username_invalid_empty():
    username = ""

    result = validate_username(username)

    assert result is False


def test_parse_log_valid_start():
    log = "14:02:03 ALICE99 Start"
    expected_result = (datetime.strptime("14:02:03", "%H:%M:%S"), "ALICE99", "Start")

    result = parse_log(log)

    assert result == expected_result


def test_parse_log_valid_end():
    log = "14:02:34 ALICE99 End"
    expected_result = (datetime.strptime("14:02:34", "%H:%M:%S"), "ALICE99", "End")

    result = parse_log(log)

    assert result == expected_result


def test_parse_log_invalid_entry():
    log = "14:02:03 ALICE99 InvalidAction"

    result = parse_log(log)

    assert result is None


def test_parse_log_invalid_username():
    log = "14:02:03 9Alice Start"

    result = parse_log(log)

    assert result is None


def test_parse_log_invalid_timestamp():
    log = "99:99:99 ALICE99 Start"

    result = parse_log(log)

    assert result is None


def test_parse_all_logs_valid_entries():
    logs = [
        "14:02:03 ALICE99 Start",
        "14:02:34 ALICE99 End",
        "14:03:02 CHARLIE Start",
        "14:03:37 CHARLIE End",
        "14:04:41 ALICE99 Start",
    ]
    expected_result = [
        (datetime.strptime("14:02:03", "%H:%M:%S"), "ALICE99", "Start"),
        (datetime.strptime("14:02:34", "%H:%M:%S"), "ALICE99", "End"),
        (datetime.strptime("14:03:02", "%H:%M:%S"), "CHARLIE", "Start"),
        (datetime.strptime("14:03:37", "%H:%M:%S"), "CHARLIE", "End"),
        (datetime.strptime("14:04:41", "%H:%M:%S"), "ALICE99", "Start"),
    ]

    result = parse_all_logs(logs)

    assert result == expected_result


def test_parse_all_logs_invalid_entries():
    logs = [
        "14:02:03 ALICE99 InvalidAction",
        "14:02:34 ALI@CE99 End",
        "14:03:02 9CHARLIE Start",
        "99:99:99 CHARLIE End",
        "14:04:41 ALICE99 Start xyz",
    ]

    result = parse_all_logs(logs)

    assert result is None


def test_parse_all_logs_empty_list():
    logs = []

    result = parse_all_logs(logs)

    assert result is None


def test_create_bin_valid_logs():
    parsed_logs = [
        (datetime.strptime("14:02:03", "%H:%M:%S"), "ALICE99", "Start"),
        (datetime.strptime("14:02:34", "%H:%M:%S"), "ALICE99", "End"),
        (datetime.strptime("14:03:02", "%H:%M:%S"), "CHARLIE", "Start"),
        (datetime.strptime("14:03:37", "%H:%M:%S"), "CHARLIE", "End"),
        (datetime.strptime("14:04:41", "%H:%M:%S"), "ALICE99", "Start"),
    ]
    expected_result = {
        "ALICE99": {
            "Start": [
                datetime.strptime("14:02:03", "%H:%M:%S"),
                datetime.strptime("14:04:41", "%H:%M:%S"),
            ],
            "End": [datetime.strptime("14:02:34", "%H:%M:%S")],
        },
        "CHARLIE": {
            "Start": [datetime.strptime("14:03:02", "%H:%M:%S")],
            "End": [datetime.strptime("14:03:37", "%H:%M:%S")],
        },
    }

    result = create_bin(parsed_logs)

    assert result == expected_result


def test_create_bin_empty_logs():
    parsed_logs = []

    result = create_bin(parsed_logs)

    assert result is None


def test_make_equal_bin_size_valid_logs():
    logs_by_user = {
        "ALICE99": {
            "Start": [
                datetime.strptime("14:02:03", "%H:%M:%S"),
                datetime.strptime("14:04:41", "%H:%M:%S"),
            ],
            "End": [datetime.strptime("14:02:34", "%H:%M:%S")],
        },
        "CHARLIE": {
            "Start": [datetime.strptime("14:03:02", "%H:%M:%S")],
            "End": [datetime.strptime("14:03:37", "%H:%M:%S")],
        },
    }
    first_log = datetime.strptime("14:02:03", "%H:%M:%S")
    last_log = datetime.strptime("14:04:41", "%H:%M:%S")

    expected_result = {
        "ALICE99": {
            "Start": [datetime(1900, 1, 1, 14, 2, 3), datetime(1900, 1, 1, 14, 4, 41)],
            "End": [datetime(1900, 1, 1, 14, 2, 34), datetime(1900, 1, 1, 14, 4, 41)],
        },
        "CHARLIE": {
            "Start": [datetime(1900, 1, 1, 14, 3, 2)],
            "End": [datetime(1900, 1, 1, 14, 3, 37)],
        },
    }

    result = make_equal_bin_size(logs_by_user, first_log, last_log)

    assert result == expected_result


def test_make_equal_bin_size_empty_logs():
    logs_by_user = {}
    first_log = datetime.strptime("14:02:03", "%H:%M:%S")
    last_log = datetime.strptime("14:04:41", "%H:%M:%S")

    result = make_equal_bin_size(logs_by_user, first_log, last_log)

    assert result is None


def test_calculate_log_time_valid_logs():
    logs_by_user = {
        "ALICE99": {
            "Start": [
                datetime.strptime("14:02:03", "%H:%M:%S"),
                datetime.strptime("14:04:58", "%H:%M:%S"),
            ],
            "End": [
                datetime.strptime("14:02:34", "%H:%M:%S"),
                datetime.strptime("14:05:02", "%H:%M:%S"),
            ],
        },
        "CHARLIE": {
            "Start": [datetime.strptime("14:03:02", "%H:%M:%S")],
            "End": [datetime.strptime("14:03:37", "%H:%M:%S")],
        },
    }
    expected_result = {"ALICE99": [31.0, 4.0], "CHARLIE": [35.0]}

    result = calculate_log_time(logs_by_user)

    assert result == expected_result


def test_calculate_log_time_empty_logs():
    logs_by_user = {}

    result = calculate_log_time(logs_by_user)

    assert result is None


def test_process_logs_valid_logs():
    logs = [
        "14:02:03 ALICE99 Start",
        "14:02:34 ALICE99 End",
        "14:03:02 CHARLIE Start",
        "14:03:37 CHARLIE End",
        "14:04:58 ALICE99 Start",
        "14:05:02 ALICE99 End",
    ]
    expected_result = {"ALICE99": [31.0, 4.0], "CHARLIE": [35.0]}

    result = process_logs(logs)

    assert result == expected_result


def test_process_logs_empty_logs():
    logs = []

    result = process_logs(logs)

    assert result is None


def test_process_logs_invalid_logs():
    logs = [
        "14:02:03 ALI@CE99 Start",
        "14:02:34 ALICE99",
        "14:03:02 CHARLIE xyz",
        "99:00:00 CHARLIE End",
        "14:04:58 ALICE99 Start abc",
        "14:05:02 1ALICE99 End",
    ]

    result = process_logs(logs)

    assert result is None


def test_process_empty_parsed_logs():
    logs = []

    result = process_logs(logs)

    assert result is None


def test_generate_report_valid_file():
    path = "test_data.txt"
    expected_result = "ALICE99 4 240\nCHARLIE 3 37"

    result = generate_report(path)

    assert result == expected_result


def test_generate_report_valid_file_with_invalid_data():
    path = "valid_file_with_invalid_data.txt"

    with open(path, "w") as f:
        f.write("xyz")

    result = generate_report(path)

    assert result is None

    os.remove(path)


def test_generate_report_empty_file():
    path = "empty.txt"

    result = generate_report(path)

    assert result is None


def test_generate_report_invalid_file():
    path = "invalid.txt"

    result = generate_report(path)

    assert result is None


def test_print_report_single_file(capsys):
    sys.argv = ["main.py", "test_data.txt"]
    expected_output = "ALICE99 4 240\nCHARLIE 3 37"

    print_report()

    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output


def test_print_report_multiple_files(capsys):
    sys.argv = ["main.py", "test_data.txt", "test_data.txt"]
    expected_output = "ALICE99 4 240\nCHARLIE 3 37\nALICE99 4 240\nCHARLIE 3 37"

    print_report()

    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output


def test_print_report_no_files(capsys):
    sys.argv = ["main.py"]
    expected_output = "Usage: python main.py <file_path>"

    with pytest.raises(SystemExit) as exc_info:
        print_report()

    assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output


def test_print_report_invalid_file(capsys):
    sys.argv = ["main.py", "invalid.txt"]
    expected_output = ""

    print_report()

    captured = capsys.readouterr()
    assert captured.out.strip() == expected_output
