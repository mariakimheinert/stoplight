import toml

RC = None
RC_FILENAME = '.stoplightrc'


def load():
    '''
    Load configuration file as TOML.
    '''
    global RC
    with open(RC_FILENAME, encoding='utf-8') as rc_file:
        RC = toml.load(rc_file)


def get(key: str) -> str | None:
    '''
    Get value of key and return None if key does not exist.
    '''
    if RC is None:
        return None
    return RC.get(key)
