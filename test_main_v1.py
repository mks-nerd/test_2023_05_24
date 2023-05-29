import os
from datetime import datetime

from main import create_bin, parse_all_logs, parse_log, read_file, validate_username

# Test files
TEST_FILE_PATH: str = "test_data.txt"
EMPTY_TEST_FILE_PATH: str = "empty_file.txt"
NON_EXISTENT_FILE_PATH: str = "non_existent_file.txt"


def test_read_existing_file():
    lines = read_file(TEST_FILE_PATH)

    assert lines is not None
    assert isinstance(lines, list)
    assert len(lines) > 0

    expected_lines = [
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
    assert lines == expected_lines


def test_read_nonexistent_file():
    lines = read_file(NON_EXISTENT_FILE_PATH)
    assert lines is None


def test_read_empty_file():
    # Create an empty file for testing
    with open(EMPTY_TEST_FILE_PATH, "w", encoding="utf-8"):
        pass

    lines = read_file(EMPTY_TEST_FILE_PATH)
    assert lines is None

    # Clean up the empty file after testing
    os.remove(EMPTY_TEST_FILE_PATH)


def test_valid_username():
    assert validate_username("xyz123") is True


def test_invalid_username_start_with_digit():
    assert validate_username("123xyz") is False


def test_invalid_username_special_characters():
    assert validate_username("abc.xyz") is False


def test_invalid_username_whitespace():
    assert validate_username("abc xyz") is False


def test_invalid_username_empty():
    assert validate_username("") is False


def test_invalid_username_start_with_special_character():
    assert validate_username("@xyz") is False


def test_invalid_username_start_with_whitespace():
    assert validate_username(" abc") is False


def test_valid_log_start_action():
    log = "14:02:03 ALICE99 Start"
    result = parse_log(log)
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], datetime)
    assert result[1] == "ALICE99"
    assert result[2] == "Start"


def test_valid_log_end_action():
    log = "14:02:34 ALICE99 End"
    result = parse_log(log)
    assert result is not None
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[0], datetime)
    assert result[1] == "ALICE99"
    assert result[2] == "End"


def test_invalid_log_missing_parts():
    log = "14:02:03 ALICE99"
    result = parse_log(log)
    assert result is None


def test_invalid_log_invalid_action():
    log = "14:02:03 ALICE99 InvalidAction"
    result = parse_log(log)
    assert result is None


def test_invalid_log_invalid_username():
    log = "14:02:03 @ALICE99 Start"
    result = parse_log(log)
    assert result is None


def test_invalid_log_invalid_timestamp():
    log = "99:99:99 ALICE99 Start"
    result = parse_log(log)
    assert result is None


def test_invalid_log_blank():
    log = ""
    result = parse_log(log)
    assert result is None


def test_valid_logs():
    logs = [
        "14:02:03 ALICE99 Start",
        "14:02:34 ALICE99 End",
        "14:03:02 CHARLIE Start",
        "14:03:37 CHARLIE End",
    ]
    result = parse_all_logs(logs)
    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 4
    for log in result:
        assert isinstance(log, tuple)
        assert len(log) == 3
        assert isinstance(log[0], datetime)
        assert isinstance(log[1], str)
        assert isinstance(log[2], str)


def test_invalid_logs():
    logs = [
        "14:02:03 ALICE99 Start xyz",
        "14:02:34 ALICE99 InvalidAction",
        "14:03:02 CH#RLIE Start",
        "14:03:37",
    ]
    result = parse_all_logs(logs)
    assert result is None


def test_empty_logs():
    logs = []
    result = parse_all_logs(logs)
    assert result is None


def test_create_bin():
    parsed_logs = [
        (datetime(2023, 5, 28, 14, 2, 3), "ALICE99", "Start"),
        (datetime(2023, 5, 28, 14, 2, 5), "CHARLIE", "End"),
        (datetime(2023, 5, 28, 14, 2, 34), "ALICE99", "End"),
        (datetime(2023, 5, 28, 14, 2, 58), "ALICE99", "Start"),
        (datetime(2023, 5, 28, 14, 3, 2), "CHARLIE", "Start"),
        (datetime(2023, 5, 28, 14, 3, 33), "ALICE99", "Start"),
        (datetime(2023, 5, 28, 14, 3, 35), "ALICE99", "End"),
        (datetime(2023, 5, 28, 14, 3, 37), "CHARLIE", "End"),
        (datetime(2023, 5, 28, 14, 4, 5), "ALICE99", "End"),
        (datetime(2023, 5, 28, 14, 4, 23), "ALICE99", "End"),
        (datetime(2023, 5, 28, 14, 4, 41), "CHARLIE", "Start"),
    ]
    result = create_bin(parsed_logs)
    assert isinstance(result, dict)

    assert "ALICE99" in result
    assert "Start" in result["ALICE99"]
    assert "End" in result["ALICE99"]
    assert len(result["ALICE99"]["Start"]) == 3
    assert len(result["ALICE99"]["End"]) == 4

    assert "CHARLIE" in result
    assert "Start" in result["CHARLIE"]
    assert "End" in result["CHARLIE"]
    assert len(result["CHARLIE"]["Start"]) == 2
    assert len(result["CHARLIE"]["End"]) == 2


def test_create_bin_empty_logs():
    parsed_logs = []
    result = create_bin(parsed_logs)
    assert result is None
