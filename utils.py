from datetime import datetime


def get_time_string():
    now = datetime.now()
    return now.strftime("%d_%m_%Y_%Hh_%Mm_%Ss")
