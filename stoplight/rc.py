import toml

rc = None


def load():
    '''
    Load configuration file as TOML.
    '''
    RC_FILENAME = '.stoplightrc'
    global rc
    rc = toml.loads(open(RC_FILENAME).read())


def get(key: str) -> str | None:
    '''
    Get value of key and return None if key does not exist.
    '''
    if rc is None:
        return None
    return rc.get(key)
