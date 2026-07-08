"""Tests for the analyzer.Log.extract function."""

import sys
from pathlib import Path
import io
from contextlib import redirect_stdout

# Ensure project root is on sys.path so tests can import analyzer
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.analyzer import Log

def test_extract():
    """Test the extract function of the Log class."""

    line = "2026-07-06 10:02:01 ERROR Database connection failed"
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    print("I am here")
    assert result == {"date": "2026-07-06",
                      "time":  "10:02:01",
                      "log_type": "ERROR",
                      "message": "Database connection failed"}

def test_extract_invalid_format():
    """Test the extract function with an invalid log line format."""

    line = "Invalid log line format"
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result is None
    
def test_extract_empty_line():
    """Test the extract function with an empty log line."""

    line = ""
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result is None
    
def test_extract_different_log_type():
    """Test the extract function with a different log type."""

    line = "2026-07-06 10:03:55 WARNING Disk usage high"
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result == {"date": "2026-07-06",
                      "time":  "10:03:55",
                      "log_type": "WARNING",
                      "message": "Disk usage high"}
    
def test_extract_additional_spaces():
    """Test the extract function with additional spaces in the log line."""

    line = "2026-07-06  10:04:15   INFO   Request completed"
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result == {"date": "2026-07-06",
                      "time":  "10:04:15",
                      "log_type": "INFO",
                      "message": "Request completed"}
    
def test_extract_special_characters_in_message():
    """Test the extract function with special characters in the log message."""

    line = "2026-07-06 10:05:10 ERROR Timeout occurred! Please check the server."
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result == {"date": "2026-07-06",
                      "time":  "10:05:10",
                      "log_type": "ERROR",
                      "message": "Timeout occurred! Please check the server."}
    
def test_extract_different_date_format():
    """Test the extract function with a different date format."""

    line = "07/06/2026 10:06:20 INFO User logged out"
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result is None  # The current regex does not support this date format
    
def test_extract_multiline_message():
    """Test the extract function with a multiline log message."""

    line = "2026-07-06 10:07:30 ERROR An error occurred:\nDetails: Connection refused"
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result == {"date": "2026-07-06",
                      "time":  "10:07:30",
                      "log_type": "ERROR",
                      "message": "An error occurred:\nDetails: Connection refused"}
    
def test_extract_log_type_case_insensitivity():
    """Test the extract function with different cases for log types."""

    line = "2026-07-06 10:08:40 info User logged in"
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result == {"date": "2026-07-06",
                      "time":  "10:08:40",
                      "log_type": "info",
                      "message": "User logged in"}
    
def test_extract_log_type_not_in_list():
    """Test the extract function with a log type not in the provided list."""

    line = "2026-07-06 10:09:50 DEBUG Debugging information"
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result == {"date": "2026-07-06",
                      "time":  "10:09:50",
                      "log_type": "DEBUG",
                      "message": "Debugging information"}
    
def test_extract_log_type_with_numbers():
    """Test the extract function with a log type that contains numbers."""

    line = "2026-07-06 10:10:00 ERROR123 An error with numbers in log type"
    log_obj = Log(["INFO", "ERROR", "WARNING"], r"logs\sample.log")
    result = log_obj.extract(line)
    assert result == {"date": "2026-07-06",
                      "time":  "10:10:00",
                      "log_type": "ERROR123",
                      "message": "An error with numbers in log type"}
    
def test_do():
    """Test the do function of the Log class with a sample log file."""

    log_types = ["INFO", "ERROR", "WARNING"]
    log_path = r"logs\sample.log"
    log_obj = Log(log_types, log_path)
    buf = io.StringIO()
    with redirect_stdout(buf):
        log_obj.do()
    assert buf.getvalue() == "===== Log Report =====\n\nINFO: 2\nERROR: 2\nWARNING: 1\n\nTotal Logs: 5\n\nMost Frequent Level: ERROR\n"

def test_do_with_empty_log_file():
    """Test the do function of the Log class with an empty log file."""

    log_types = ["INFO", "ERROR", "WARNING"]
    log_path = r"logs\empty.log"
    log_obj = Log(log_types, log_path)
    buf = io.StringIO()
    with redirect_stdout(buf):
        log_obj.do()
    assert buf.getvalue() == "===== Log Report =====\n\nINFO: 0\nERROR: 0\nWARNING: 0\n\nTotal Logs: 0\n\nMost Frequent Level: N/A\n"
    
def test_do_with_nonexistent_log_file():
    """Test the do function of the Log class with a nonexistent log file."""

    log_types = ["INFO", "ERROR", "WARNING"]
    log_path = r"logs\nonexistent.log"
    log_obj = Log(log_types, log_path)
    buf = io.StringIO()
    with redirect_stdout(buf):
        log_obj.do()
    assert buf.getvalue() == "No log files found.\n"
    
def test_do_with_invalid_log_lines():
    """Test the do function of the Log class with a log file containing invalid log lines."""

    log_types = ["INFO", "ERROR", "WARNING"]
    log_path = r"logs\invalid_lines.log"
    log_obj = Log(log_types, log_path)
    buf = io.StringIO()
    with redirect_stdout(buf):
        log_obj.do()
    assert buf.getvalue() == "Invalid log file\n"