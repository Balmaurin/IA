import datetime


def write_log(event: str, user: str = "system"):
    with open("/tmp/sheily_event.log", "a") as f:
        f.write(f"{datetime.datetime.now()} | {user} | {event}\n")
