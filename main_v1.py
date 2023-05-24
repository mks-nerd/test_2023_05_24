import sys
from datetime import datetime


def generate_report(data_to_print):
    for user_name, user_data in data_to_print.items():
        print(user_name, user_data["session"], user_data["total_time"])


def read_file(path: str) -> list[str] | None:
    """read txt file and returns a list of all lines"""
    try:
        with open(path) as file:
            lines: list[str] = file.readlines()
    except FileNotFoundError:
        return None
    return lines


def parse_log(log: str) -> tuple[datetime, str, str] | None:
    """parse string into time, user_name and action"""
    log_parts = log.strip().split()
    if len(log_parts) != 3 or log_parts[-1] not in ["Start", "End"]:
        return None

    timestamp_str, user_name, action = log_parts
    try:
        time = datetime.strptime(timestamp_str, "%H:%M:%S")
    except ValueError:
        return None
    return time, user_name, action


def process_logs(logs):
    logs_by_user = {}
    data = {}
    parsed_logs = [parse_log(log) for log in logs]
    parsed_logs = [parsed_log for parsed_log in parsed_logs if parsed_log]
    first_parsed_log = parsed_logs[0][0]
    last_parsed_log = parsed_logs[-1][0]

    for parsed_log in parsed_logs:
        timestamp, user, action = parsed_log
        user = logs_by_user.setdefault(user, {})
        action = user.setdefault(action, [])
        action.append(timestamp)

    for keys, items in logs_by_user.items():
        start_items = items.setdefault("Start", [])
        end_items = items.setdefault("End", [])

        for start, end in zip(start_items, end_items):
            if start > end:
                start_items.insert(0, first_parsed_log)

        start_items_length = len(start_items)
        end_items_length = len(end_items)

        while start_items_length != end_items_length:
            if start_items_length > end_items_length:
                end_items.append(last_parsed_log)
                end_items_length += 1
            else:
                start_items.insert(0, first_parsed_log)
                start_items_length += 1

    for user, items in logs_by_user.items():
        user = data.setdefault(user, [])
        for start, end in zip(items.get("Start"), items.get("End")):
            user.append((end - start).total_seconds())

    for user, items in data.items():
        print(user, len(items), int(sum(items)))

    return logs_by_user


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fair_billing.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    all_logs = read_file(path=file_path)
    data = process_logs(logs=all_logs)
    # print(data)
