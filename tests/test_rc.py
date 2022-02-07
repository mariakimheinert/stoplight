from importlib import reload
import toml

from stoplight import rc


def test_load_opens_stoplightrc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    mocker.patch('os.path.exists', return_value=True)
    rc.load()
    mock_open.assert_called_once_with('.stoplightrc', encoding='utf-8')


def test_get_load_not_called_returns_none(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    reload(rc)
    assert rc.get('token') is None


def test_get_empty_rc_returns_none(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    rc.load()
    assert rc.get('token') is None


def test_get_returns_value(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'token': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    rc.load()
    assert rc.get('token') == 'test'
