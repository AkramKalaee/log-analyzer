from analyzer import Log


def main():
    """Main function to create a log analyzer object and call the do method."""

    log_types = ["INFO", "ERROR", "WARNING"] # Define the log types to analyze
    log_path = r"logs\sample.log" # Define the path to the log file to analyze
    log_obj = Log(log_types, log_path) # Create an instance of the Log class
    log_obj.do() # Call the do method to analyze the log file and generate a report


if __name__ == "__main__":
    main()
