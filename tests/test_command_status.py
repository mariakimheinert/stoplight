from typer.testing import CliRunner
import toml
import pytest

from stoplight.run import app
from stoplight.run import run_status


runner = CliRunner()


@pytest.fixture(autouse=True)
def patch_run(mocker):
    mocker.patch('stoplight.run.run_status')
    yield


def test_status_errs_if_missing_token(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['status', '--org', 'test', '--assignment-title', 'test'])
    assert result.exit_code == 1


def test_status_errs_if_missing_organization(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['status', '--token', 'test', '--assignment-title', 'test'])
    assert result.exit_code == 1


def test_status_errs_if_missing_assignment(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['status', '--token', 'test', '--org', 'test'])
    assert result.exit_code == 1


def test_status_does_not_err_if_token_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'token': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['status', '--org', 'test', '--assignment-title', 'test'])
    assert result.exit_code == 0


def test_status_does_not_err_if_org_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'org': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['status', '--token', 'test', '--assignment-title', 'test'])
    assert result.exit_code == 0


def test_status_does_not_err_if_assignment_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'assignment_title': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['status', '--token', 'test', '--org', 'test'])
    assert result.exit_code == 0
