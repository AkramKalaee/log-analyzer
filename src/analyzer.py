import glob
import re


class Log:
    """A class to analyze log files and generate a report based on the log types."""

    def __init__(self, log_types, path):
        """Initialize the log analyzer with the given log types and path to the log file.
    
        Args:
            log_types (list[str]): A list of log types to analyze (e.g., ["INFO", "WARNING", "ERROR"]).
            path (str): The path to the log file to analyze.
        """

        self.types_dict = {}
        for log_type in log_types:
            self.types_dict[log_type] = 0

        self.path = path
        self.total_logs = 0

    def extract(self, info: str) -> dict[str, str] | None:
        """Extract the date, time, log type, and message from a log line.
        If the log line does not match the expected format, return None.
        
        Args:
            info (str): A log line in the format "YYYY-MM-DD HH:MM:SS LOG_TYPE MESSAGE".
            
        Returns:
            dict[str, str] | None: A dictionary with keys "date", "time",
            "log_type", and "message".
        """

        date = r"\d{4}-\d{2}-\d{2}"
        time = r"\d{2}:\d{2}:\d{2}"
        log_type = r"\w+"
        message = r".*"
        pattern = rf"({date})\s+({time})\s+({log_type})\s+({message})"
        match = re.match(pattern, info)

        if not match:
            return None

        return {
            "date": match.group(1),
            "time": match.group(2),
            "log_type": match.group(3),
            "message": match.group(4)
        }

    def do(self) -> None:
        """Read the current log file, call the extract function for each line of the log, 
        and then call the make_report function.
        
        sample input:
        # 2026-07-06 10:01:12 INFO User logged in
        # 2026-07-06 10:02:01 ERROR Database connection failed
        # 2026-07-06 10:03:55 WARNING Disk usage high
        # 2026-07-06 10:04:15 INFO Request completed
        # 2026-07-06 10:05:10 ERROR Timeout occurred

        sample output:
        # ===== Log Report =====

        # INFO: 2
        # WARNING: 1
        # ERROR: 2

        # Total Logs: 5

        # Most Frequent Level: ERROR
        """

        # read line by line
        all_in_one = glob.glob(self.path)

        if not all_in_one:
            print("No log files found.")
            return

        with open(all_in_one[0], "r", encoding="utf-8") as f:
            content = f.read().split("\n")

        for line in content:
            if line.strip():  # Skip empty lines
                extracted_data_dict = self.extract(line)
                if not extracted_data_dict:
                    continue
                log_type = extracted_data_dict["log_type"]
                if log_type in self.types_dict:
                    self.types_dict[log_type] += 1
                self.total_logs += 1

        self.make_report()

    def make_report(self) -> None:
        """Make a report for the current log file and print it."""

        report = "===== Log Report =====\n\n"
        most_frequent_level = ""
        most_frequent = 0
        for key, value in self.types_dict.items():
            report += f"{key}: {value}\n"
            if most_frequent <= value:
                most_frequent_level = key
                most_frequent = value

        report += "\n\n"
        report += f"Total Logs: {self.total_logs}"
        report += "\n\n"
        report += f"Most Frequent Level: {most_frequent_level}"

        print(report)
