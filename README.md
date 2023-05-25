# Fair Billing

This is a test repository created on May 24, 2023, for generating report out of logs file(s).

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Code-Flow](#Code-Flow)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

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

1. The necessary modules are imported:
   - `sys` for system-related functionality.
   - `datetime` for working with date and time objects.

2. The `read_file` function is defined. It takes a file path as input, attempts to open and read the file, and returns a list of all the lines read from the file. If the file is not found, it returns `None`.

3. The `parse_log` function is defined. It takes a log string as input and attempts to parse it into a tuple containing a `datetime` object, a username, and an action. If the log cannot be parsed due to incorrect formatting, it returns `None`.

4. The `process_logs` function is defined. It takes a list of log strings as input and processes them to generate a summary of the logs. It returns a dictionary where the keys are usernames, and the values are lists of durations (in seconds) for each user's actions. If the log list is empty or cannot be parsed, it returns `None`.

5. The `generate_report` function is defined. It takes a file path as input, reads the log file using the `read_file` function, processes the logs using the `process_logs` function, and generates a report based on the processed data. The report is returned as a string.

6. The `print_report` function is defined. It checks if the script is executed with the correct command-line arguments (at least one file path) and calls the `generate_report` function for each file path provided. It then prints the generated reports.

7. The script entry point is checked using the `__name__ == "__main__"` condition. If the script is being executed directly (not imported as a module), it calls the `print_report` function.

In summary, this script reads log files, processes the logs to generate a summary, and prints a report with the number of actions and total durations for each user. Multiple file paths can be provided as command-line arguments.

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

2. Open a terminal or command prompt and navigate to the project's root directory.

3. Run the script using the Python interpreter:
   ```
   python main.py location/to/file.txt
   ```

4. The script will process the log file and generate a report with the users, the number of sessions, and the minimum possible total duration of their sessions in seconds. The report will be printed to the console.

5. Review the generated report to analyze the data.
6. Run tests from terminal using:
   ```
   # Required: Virtual Environment with dependecies installed from requirments.txt
   
   coverage run -m pytest
   ```
7. View the tests coverage using:
   ```
   coverage report
   ```

Feel free to modify the script or customize it according to your specific requirements.

## Contributing

Contributions to this repository are currently not accepted as it is meant for personal experimentation and learning. However, if you would like to provide feedback or report issues related to the log parsing script, you can do so by creating an issue on the repository's [issue tracker](https://github.com/mks-nerd/test_2023_05_24/issues).

## License

The content of this repository is not bound by any specific license. It is provided as-is for learning and experimental purposes. For more details, please contact the repository owner for clarification.
