import datetime


def log_chat_event(user, prompt, response, fallback=False):
    with open("/tmp/sheily_chat.log", "a") as f:
        f.write(f"{datetime.datetime.now()} | {user} | {prompt} | {response} | {'fallback' if fallback else 'local'}\n")
