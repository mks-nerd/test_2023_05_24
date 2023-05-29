# Fair Billing

This is a test repository created on May 24, 2023, for generating a report out of log file(s).

## Table of Contents
- [Introduction](#introduction)
- [Code-Flow](#Code-Flow)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Notes](#Notes)

## Introduction

The problem revolves around fair billing for a hosted application provider. The provider charges users based on the duration of their sessions, with a per-second usage fee. The usage data is stored in a log file that includes the start and end times of sessions, along with the username and session status (Start or End). However, there are some challenges with the log file:

1. Missing Pairing Indicators: The log file doesn't indicate which start and end entries are paired together. This means that it's unclear which "Start" corresponds to which "End" entry.

2. Overlapping Sessions: The log file may not cover the entire duration of all sessions due to regular rewriting. Consequently, there may be "End" entries for sessions that started before the log file began, lacking the corresponding "Start" entry. Similarly, there might be "Start" entries for sessions that are still in progress when the log file is retrieved, without a subsequent "End" entry.

The task is to generate a report that includes the usernames, the number of sessions for each user, and the minimum possible total duration of their sessions in seconds, based on the available data in the log file. Here are a few additional considerations:

- If there is an "End" entry without a corresponding "Start" entry, assume the start time to be the earliest time recorded in the file.
- If there is a "Start" entry without a corresponding "End" entry, assume the end time to be the latest time recorded in the file.

Invalid or irrelevant lines in the log file should be ignored during the calculations. The program should take the path to the log file as a command line parameter and provide the desired report.

## Code-Flow
The `main.py` file contains a script for generating and printing a report based on log files. Here's the flow of the code:

1. The main module defines various functions for different tasks such as reading a file, validating usernames, parsing log entries, organizing logs, calculating log times, and generating reports.

2. The `read_file` function reads the contents of a file specified by the path and returns the lines as a list of strings.

3. The `validate_username` function checks if a username string is valid by matching it against a regular expression pattern.

4. The `parse_log` function parses a log entry string and extracts the timestamp, username, and action. It returns a tuple containing the parsed data or None if the log entry is invalid.

5. The `parse_all_logs` function takes a list of log entry strings, iterates over them, and parses each log using the `parse_log` function. It returns a list of tuples containing the parsed log data or None if no valid log entries were found.

6. The `create_bin` function creates a nested dictionary structure to organize the parsed logs by user and action.

7. The `make_equal_bin_size` function adjusts the bin sizes for start and end logs of each user to ensure equal lengths by padding with the first and last log if necessary.

8. The `calculate_log_time` function calculates the time duration for each user's log entries based on the start and end timestamps.

9. The `process_logs` function performs the processing steps by calling the above functions in sequence. It returns a dictionary where the keys are usernames and the values are lists of durations, or None if the input logs are None or the processing steps result in empty data.

10. The `generate_report` function generates a report based on the log data provided in a file. It reads the file using `read_file`, processes the logs using `process_logs`, and generates a string representation of the report.

11. The `print_report` function prints the generated report for each specified log file path. It takes the file paths as command-line arguments, calls `generate_report` for each path, and prints the report if it is not None.

12. Finally, the code checks if the module is being executed as the main script (`__name__ == "__main__"`) and calls the `print_report` function.

Overall, the code reads log files, processes the logs, calculates log times, and generates reports based on the log data.
## Installation

To use the script in this repository, follow the instructions below:

1. Clone the repository using Git:
   ```
   git clone https://github.com/mks-nerd/test_2023_05_24.git
   ```

2. Navigate to the project's root directory:
   ```
   cd test_2023_05_24
   ```

3. [Optional] Set up any necessary dependencies or environment configurations.

4. You are ready to use the script.

## Usage

To run the script and generate the report, follow these steps:

1. Make sure you have a log file containing the necessary data.

2. Make sure you have `python --version #python >= 3.7` installed.

3. Open a terminal or command prompt and navigate to the project's root directory.

4. Run the script using the Python interpreter:
   ```
   python main.py test_data.txt
   ```
   or 
   ```
   python3 main.py test_data.txt
   ```
   or
   ```
   py main.py test_data.txt
   ```
   The Output will be
   ```
   ALICE99 4 240
   CHARLIE 3 37
   ```
5. The script will process the log file and generate a report with the users, the number of sessions, and the minimum possible total duration of their sessions in seconds. The report will be printed to the console.

6. Review the generated report to analyze the data.
7. Run tests from the terminal using:
   ```
   # Required: Virtual Environment with dependecies installed from requirments.txt
   
   coverage run -m pytest
   ```
8. View the test coverage using:
   ```
   coverage report
   ```

Feel free to modify the script or customize it according to your specific requirements.

## Contributing

Contributions to this repository are currently not accepted as it is meant for personal experimentation and learning. However, if you would like to provide feedback or report issues related to the log parsing script, you can do so by creating an issue on the repository's [issue tracker](https://github.com/mks-nerd/test_2023_05_24/issues).

## License

Any specific license does not bind the content of this repository.
It is provided as-is for submitting test purpose.
For more details, please contact the repository owner for clarification.

## Notes

1. Action Validation
   - User actions must be either "Start" or "End". The utility will discard Any action other than these two values.

2. Timestamp Validation
   - Validates timestamps to ensure they are in a valid time format. If a timestamp is not a valid time, it will be discarded by the utility. 

3. Username Validation
   - Validates the given username string to ensure it consists of alphanumeric characters with no specific length criteria.