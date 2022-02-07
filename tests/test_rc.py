from importlib import reload
import os
import toml

from stoplight import rc


def test_load_opens_stoplightrc(mocker):
    mocker.patch('stoplight.rc.rc_filename', return_value='.stoplightrc')
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    rc.load()
    mock_open.assert_called_once_with('.stoplightrc', encoding='utf-8')


def test_rc_filename_local_stoplightrc_exists_returns_local_stoplightrc(mocker):
    mocker.patch('os.path.exists', return_value=True)
    assert rc.rc_filename() == '.stoplightrc'


def test_rc_filename_local_stoplightrc_not_exists_returns_home_stoplightrc(mocker):
    mocker.patch('os.path.exists', side_effect=[False, True])
    assert rc.rc_filename() == f'{os.path.expanduser("~")}/.stoplightrc'


def test_rc_filename_no_stoplightrc_returns_none(mocker):
    mocker.patch('os.path.exists', side_effect=[False, False])
    assert rc.rc_filename() is None


def test_get_load_not_called_returns_none(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    reload(rc)
    assert rc.get('token') is None


def test_get_empty_rc_returns_none(mocker):
    mocker.patch('stoplight.rc.rc_filename', return_value='.stoplightrc')
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    rc.load()
    assert rc.get('token') is None


def test_get_returns_value(mocker):
    mocker.patch('stoplight.rc.rc_filename', return_value='.stoplightrc')
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'token': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    rc.load()
    assert rc.get('token') == 'test'
