from datetime import datetime
import inspect


def log(message, status=None):
    time_now = datetime.now().strftime("%H:%M:%S")
    file_name = inspect.stack()[1].filename.split("/")[-1]
    file_name = file_name + " " * (40 - len(file_name))
    file_name = file_name[:40]

    if status == "info":
        print(f"\033[94m{time_now} | {file_name} | {message}\033[0m")
    elif status == "success":
        print(f"\033[92m{time_now} | {file_name} | {message}\033[0m")
    elif status == "danger":
        print(f"\033[91m{time_now} | {file_name} | {message}\033[0m")
    elif status == "warning":
        print(f"\033[93m{time_now} | {file_name} | {message}\033[0m")
    else:
        print(f"{time_now} | {file_name} | {message}")

    # create a print with tabs
