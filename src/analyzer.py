import glob
import re

class log:
    def __init__(self, log_types, path):
        self.types_dict = {}
        for log_type in log_types:
            self.types_dict[log_type] = 0

        self.path = path
        self.total_logs = 0

    def extract(self, log):
        date = r"\d{4}-\d{2}-\d{2}"
        time = r"\d{2}:\d{2}:\d{2}"
        log_type = r"\w+"
        message = r".*"
        pattern = rf"({date})\s+({time})\s+({log_type})\s+({message})"
        match = re.match(pattern, log)

        if not match:
            return None

        return {
            "date": match.group(1),
            "time": match.group(2),
            "log_type": match.group(3),
            "message": match.group(4)
        }

    # sample input:
    # 2026-07-06 10:01:12 INFO User logged in
    # 2026-07-06 10:02:01 ERROR Database connection failed
    # 2026-07-06 10:03:55 WARNING Disk usage high
    # 2026-07-06 10:04:15 INFO Request completed
    # 2026-07-06 10:05:10 ERROR Timeout occurred

    # sample output:
    # ===== Log Report =====

    # INFO: 2
    # WARNING: 1
    # ERROR: 2

    # Total Logs: 5

    # Most Frequent Level: ERROR

    def do(self):
        # read line by line
        all_in_one = glob.glob(self.path)

        with open(all_in_one[0], "r") as f:
            content = f.read().split("\n")

        for line in content:
            extracted_data_dict = self.extract(line)
            log_type = extracted_data_dict["log_type"]
            if log_type in self.types_dict:
                self.types_dict[log_type] += 1
            self.total_logs += 1

        self.make_report()

    def make_report(self):
        pass
        