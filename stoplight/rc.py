import os
import toml

RC = None


def load():
    '''
    Load configuration file as TOML.
    '''
    global RC
    rc_filename = '.stoplightrc'
    if not os.path.exists(rc_filename):
        rc_filename = f'{os.path.expanduser("~")}/{rc_filename}'
    if os.path.exists(rc_filename):
        with open(rc_filename, encoding='utf-8') as rc_file:
            RC = toml.load(rc_file)


def get(key: str) -> str | None:
    '''
    Get value of key and return None if key does not exist.
    '''
    if RC is None:
        return None
    return RC.get(key)
