from typer.testing import CliRunner
import toml
import pytest

from stoplight.run import app


runner = CliRunner()


@pytest.fixture(autouse=True)
def patch_run(mocker):
    mocker.patch('stoplight.run.run_green')
    yield


def test_green_errs_if_missing_token(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['green', '--org', 'test', '--assignment-title', 'test', 'test'])
    assert result.exit_code == 1


def test_green_errs_if_missing_organization(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['green', '--token', 'test', '--assignment-title', 'test', 'test'])
    assert result.exit_code == 1


def test_green_errs_if_missing_assignment(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({}))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['green', '--token', 'test', '--org', 'test', 'test'])
    assert result.exit_code == 1


def test_green_does_not_err_if_token_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'token': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['green', '--org', 'test', '--assignment-title', 'test', 'test'])
    assert result.exit_code == 0


def test_green_does_not_err_if_org_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'org': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['green', '--token', 'test', '--assignment-title', 'test', 'test'])
    assert result.exit_code == 0


def test_green_does_not_err_if_assignment_in_rc(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'assignment_title': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['green', '--token', 'test', '--org', 'test', 'test'])
    assert result.exit_code == 0


def test_green_errs_if_neither_all_nor_students_given(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'token': 'test',
        'org': 'test',
        'assignment_title': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['green'])
    assert result.exit_code == 1


def test_green_does_not_err_if_all_given(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'token': 'test',
        'org': 'test',
        'assignment_title': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['green', '--all'])
    assert result.exit_code == 0


def test_green_does_not_err_if_students_given(mocker):
    mock_open = mocker.mock_open(read_data=toml.dumps({
        'token': 'test',
        'org': 'test',
        'assignment_title': 'test'
    }))
    mocker.patch('builtins.open', mock_open)
    result = runner.invoke(
        app, ['green', 'testuser', 'testuser'])
    assert result.exit_code == 0
