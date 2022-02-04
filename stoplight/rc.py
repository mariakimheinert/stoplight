import toml
from typing import Dict

rc = None
def load() -> Dict:
    '''
    Load configuration file as TOML.
    '''
    RC_FILENAME = '.stoplightrc'
    global rc
    rc = toml.loads(open(RC_FILENAME).read())


def get(key: str) -> str:
    '''
    Get value of key and return None if key does not exist.
    '''
    return rc.get(key)
