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
    first_log = None
    for log in logs:
        parsed_log = parse_log(log)
        if parsed_log:
            first_log = (parsed_log[0], parsed_log[2])
            break

    for log in logs:
        parsed_log = parse_log(log)
        if parsed_log:
            user_logs = logs_by_user.setdefault(parsed_log[1], [])
            user_logs.append([parsed_log[0], parsed_log[2]])

    all_data = {}
    for user_name, user_logs in logs_by_user.items():
        user_data = []
        last_timestamp = None
        last_action = None
        unused_start = None

        for log in user_logs:
            timestamp = log[0]
            action = log[1]

            if last_action == "End" and action == "Start":
                if unused_start is None:
                    unused_start = log
                else:
                    user_data.append((timestamp - timestamp).total_seconds())

            elif last_action != "Start" and action == "End":
                if unused_start:
                    user_data.append((timestamp - unused_start[0]).total_seconds())
                    unused_start = None
                else:
                    if first_log:
                        user_data.append((timestamp - first_log[0]).total_seconds())

            elif last_action != "Start" and action == "Start" and len(user_logs) == 1:
                user_data.append((timestamp - timestamp).total_seconds())

            elif last_action == "Start" and action == "End":
                user_data.append((timestamp - last_timestamp).total_seconds())

            last_timestamp, last_action = timestamp, action

        all_data[user_name] = {
            "session": len(user_data),
            "total_time": int(sum(user_data)),
        }

    return all_data


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fair_billing.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    all_logs = read_file(path=file_path)
    data = process_logs(logs=all_logs)
    generate_report(data_to_print=data)
