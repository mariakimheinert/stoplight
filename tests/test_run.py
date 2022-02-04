from typer.testing import CliRunner
import typer
import toml
from importlib import reload

from stoplight import run as stoplight
from stoplight.run import app
from stoplight import rc


runner = CliRunner()


def test_generate_headers_contains_expected_keys():
    headers = stoplight.generate_headers('', '')
    assert 'Authorization' in headers
    assert 'Accept' in headers


def test_red_errs_if_missing_token(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['red', '--org', 'test', '--assignment', 'test'])
    assert result.exit_code == 1


def test_red_errs_if_missing_organization(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['red', '--token', 'test', '--assignment', 'test'])
    assert result.exit_code == 1


def test_red_errs_if_missing_assignment(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['red', '--token', 'test', '--org', 'test'])
    assert result.exit_code == 1


def test_red_does_not_err_if_token_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'token': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['red', '--org', 'test', '--assignment', 'test'])
    assert result.exit_code == 0


def test_red_does_not_err_if_org_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'org': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['red', '--token', 'test', '--assignment', 'test'])
    assert result.exit_code == 0


def test_red_does_not_err_if_assignment_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'assignment': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['red', '--token', 'test', '--org', 'test'])
    assert result.exit_code == 0


def test_green_errs_if_missing_token(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['green', '--org', 'test', '--assignment', 'test', 'test'])
    assert result.exit_code == 1


def test_green_errs_if_missing_organization(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['green', '--token', 'test', '--assignment', 'test', 'test'])
    assert result.exit_code == 1


def test_green_errs_if_missing_assignment(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['green', '--token', 'test', '--org', 'test', 'test'])
    assert result.exit_code == 1


def test_green_does_not_err_if_token_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'token': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['green', '--org', 'test', '--assignment', 'test', 'test'])
    assert result.exit_code == 0


def test_green_does_not_err_if_org_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'org': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['green', '--token', 'test', '--assignment', 'test', 'test'])
    assert result.exit_code == 0


def test_green_does_not_err_if_assignment_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'assignment': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(app, ['green', '--token', 'test', '--org', 'test', 'test'])
    assert result.exit_code == 0

