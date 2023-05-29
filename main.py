"""
This module provides functions for reading log files, parsing log entries,
calculating log times, and generating reports based on the log data.
"""

import logging
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple


def read_file(path: str) -> Optional[List[str]]:
    """
    Reads the contents of a file specified by the given path and returns the lines as a list of strings.

    Args:
        path (str): The path to the file.

    Returns:
        Optional[List[str]]: A list of strings representing the lines of the file. None if there was an error while reading the file.
    """
    try:
        with open(path, encoding="utf-8") as file:
            lines: List[str] = file.readlines()
    except Exception as e:
        logging.error("An error occurred while reading the file: %s", e)
        return None

    if len(lines) == 0:
        return None

    return lines


def validate_username(username: str) -> bool:
    """
    Validates the given username string against a regular expression pattern and determines if it is valid.

    Args:
        username (str): The username string to validate.

    Returns:
        bool: True if the username is valid, False otherwise.
    """
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9]*$", username):
        return False
    return True


def parse_log(log: str) -> Optional[Tuple[datetime, str, str]]:
    """
    Parses a log entry string and extracts the timestamp, username, and action.

    Args:
        log (str): The log entry string.

    Returns:
        Optional[Tuple[datetime, str, str]]:
        A tuple containing the parsed timestamp (datetime object), username (str), and action
        (str).
        None if the log entry is invalid or cannot be parsed.
    """

    log_parts: List[str] = log.strip().split()

    if (
        len(log_parts) != 3
        or log_parts[-1] not in ["Start", "End"]
        or not validate_username(log_parts[1])
    ):
        return None

    timestamp_str, user_name, action = log_parts

    try:
        time: datetime = datetime.strptime(timestamp_str, "%H:%M:%S")
    except ValueError:
        return None

    return time, user_name, action


def parse_all_logs(logs: List[str]) -> Optional[List[Tuple[datetime, str, str]]]:
    """
    Parses a list of log entries and returns a list of tuples containing the parsed timestamp, username, and action.

    Args:
        logs (List[str]): A list of log entry strings.

    Returns:
        Optional[List[Tuple[datetime, str, str]]]:
        A list of tuples containing the parsed timestamp (datetime object), username (str), and action
        (str).
        None if no valid log entries were found.
    """
    parsed_logs: List[Tuple[datetime, str, str]] = []

    for log in logs:
        parsed_log: Optional[Tuple[datetime, str, str]] = parse_log(log)
        if parsed_log:
            parsed_logs.append(parsed_log)

    if len(parsed_logs) == 0:
        return None

    return parsed_logs


def create_bin(
    parsed_logs: List[Tuple[datetime, str, str]]
) -> Optional[Dict[str, Dict[str, List[datetime]]]]:
    """
    Creates a nested dictionary structure to organize the parsed logs by user and action.

    Args:
        parsed_logs (List[Tuple[datetime, str, str]]): A list of tuples containing the parsed logs.

    Returns:
        Optional[Dict[str, Dict[str, List[datetime]]]]:
        A nested dictionary structure where logs are organized by user and action.
        None if no logs were provided.
    """
    logs_by_user: Dict[str, Dict[str, List[datetime]]] = {}

    for parsed_log in parsed_logs:
        timestamp, user, action = parsed_log
        user_bin = logs_by_user.setdefault(user, {})
        action_bin = user_bin.setdefault(action, [])
        action_bin.append(timestamp)

    if len(logs_by_user) == 0:
        return None

    return logs_by_user


def make_equal_bin_size(
    logs_by_user: Dict[str, Dict[str, List[datetime]]],
    first_log: datetime,
    last_log: datetime,
) -> Optional[Dict[str, Dict[str, List[datetime]]]]:
    """
    Adjusts the bin sizes for start and end logs of each user to ensure equal lengths,
    by padding with the first and last log if necessary.

    Args:
        logs_by_user (Dict[str, Dict[str, List[datetime]]]):
        A nested dictionary structure containing logs organized by user and action.
        first_log (datetime): The first log entry timestamp.
        last_log (datetime): The last log entry timestamp.

    Returns:
        Optional[Dict[str, Dict[str, List[datetime]]]]: The modified logs_by_user dictionary with equal bin sizes.
        None if no logs were provided.
    """
    for _keys, items in logs_by_user.items():
        start_items = items.setdefault("Start", [])
        end_items = items.setdefault("End", [])

        for start, end in zip(start_items, end_items):
            if start > end:
                start_items.insert(0, first_log)

        start_items_length: int = len(start_items)
        end_items_length: int = len(end_items)

        while start_items_length != end_items_length:
            if start_items_length > end_items_length:
                end_items.append(last_log)
                end_items_length += 1
            else:
                start_items.insert(0, first_log)
                start_items_length += 1

    if len(logs_by_user) == 0:
        return None

    return logs_by_user


def calculate_log_time(
    logs_by_user: Dict[str, Dict[str, List[datetime]]]
) -> Optional[Dict[str, List[float]]]:
    """
    Calculates the time duration for each user's log entries based on the start and end timestamps.

    Args:
        logs_by_user (Dict[str, Dict[str, List[datetime]]]):
        A nested dictionary structure containing logs organized by user and action.

    Returns:
        Optional[Dict[str, List[float]]]:
        A dictionary where the keys are usernames (str)
        and the values are lists of float values representing the duration
        (in seconds) between start and end timestamps for each user's log entries.
        None if no log data is provided.
    """
    data: Dict[str, List[float]] = {}

    for user, items in logs_by_user.items():
        user_bucket = data.setdefault(user, [])
        for start, end in zip(items.get("Start", []), items.get("End", [])):
            user_bucket.append((end - start).total_seconds())

    if len(data) == 0:
        return None

    return data


def process_logs(logs: List[str]) -> Optional[Dict[str, List[float]]]:
    """
    Processes the logs by performing the following steps:
    1. Parses the log entries.
    2. Organizes the logs by user and action.
    3. Adjusts the bin sizes to ensure equal lengths.
    4. Calculates the time duration for each user's log entries.

    Args:
        logs (List[str]): A list of log entry strings.

    Returns:
        Optional[Dict[str, List[float]]]:
        A dictionary where the keys are usernames (str)
        and the values are lists of float values representing the duration
        (in seconds) between start and end timestamps for each user's log entries.
        None if the input logs are None or the processing steps result in empty data.
    """
    if logs is None:
        return None

    parsed_logs: Optional[List[Tuple[datetime, str, str]]] = parse_all_logs(logs=logs)

    if parsed_logs is None:
        return None

    logs_by_user: Optional[Dict[str, Dict[str, List[datetime]]]] = create_bin(
        parsed_logs=parsed_logs
    )

    if logs_by_user is None:
        return None

    logs_by_user = make_equal_bin_size(
        logs_by_user=logs_by_user,
        first_log=parsed_logs[0][0],
        last_log=parsed_logs[-1][0],
    )

    if logs_by_user is None:
        return None

    data: Optional[Dict[str, List[float]]] = calculate_log_time(
        logs_by_user=logs_by_user
    )

    return data


def generate_report(path: str) -> Optional[str]:
    """
    Generates a report based on the log data provided in a file.

    Args:
        path (str): The path to the log file.

    Returns:
        Optional[str]: A string containing the generated report.
        None if there was an error reading the file or the log data processing resulted in empty data.
    """
    text_to_print: str = ""
    all_logs: Optional[List[str]] = read_file(path=path)

    if all_logs is None:
        return None

    summary: Optional[Dict] = process_logs(logs=all_logs)

    if summary is None:
        return None

    for user_name, user_data in summary.items():
        text: str = f"{user_name} {len(user_data)} {int(sum(user_data))}\n"
        text_to_print += text

    text_to_print = text_to_print.strip()

    return text_to_print


def print_report() -> None:
    """
    Prints the generated report for each specified log file path.

    Returns:
        None
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    file_paths: List[str] = sys.argv[1:]

    for file_path in file_paths:
        report: Optional[str] = generate_report(path=file_path)
        if report:
            print(report)


if __name__ == "__main__":
    print_report()
