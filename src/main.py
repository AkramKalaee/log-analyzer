from analyzer import log

def main():
    log_types = ["INFO", "ERROR", "WARNING"]
    log_path = r"logs\sample.log"
    log_obj = log(log_types, log_path)
    log_obj.do()

if __name__ == "__main__":
    main()
    