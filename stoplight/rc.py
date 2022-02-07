import os
import toml

RC = None


def load():
    """
    Load configuration file as TOML.
    """
    global RC
    name = rc_filename()
    if name:
        with open(name, encoding='utf-8') as rc_file:
            RC = toml.load(rc_file)


def rc_filename() -> str | None:
    """
    Return either local or home .stoplightrc file or None if neither exist.
    """
    name = '.stoplightrc'
    if not os.path.exists(name):
        name = f'{os.path.expanduser("~")}/{name}'
    if os.path.exists(name):
        return name
    return None


def get(key: str) -> str | None:
    """
    Get value of key and return None if key does not exist.
    """
    if RC is None:
        return None
    return RC.get(key)
