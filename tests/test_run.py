import pytest

from stoplight.repo import AssignmentRepo
from stoplight.run import run_green, run_status


def test_green_all_true_calls_get_all(mocker):
    mocker.patch('stoplight.repo.AssignmentRepo.get_all', return_value=[])
    run_green(token='test',
              org='testorg',
              assignment_title='testassignment',
              all=True,
              students=[])
    AssignmentRepo.get_all.assert_called()


def test_green_all_false_calls_get(mocker):
    mocker.patch('stoplight.repo.AssignmentRepo.get', return_value=None)
    run_green(token='test',
              org='testorg',
              assignment_title='testassignment',
              all=False,
              students=['testuser'])
    AssignmentRepo.get.assert_called()


def test_run_status_uses_repos(mocker, capsys):
    repo = AssignmentRepo(token='test', org='testorg',
                          name='testassignment-testuser', assignment_title='testassignment')
    repo.student_permission = mocker.MagicMock(return_value='write')
    repos = [repo]
    run_status(repos=repos)
    captured = capsys.readouterr()
    assert 'testassignment-testuser' in captured.out
    assert 'testuser' in captured.out
    assert 'write' in captured.out


def test_run_status_missing_token_raises():
    with pytest.raises(ValueError):
        run_status(org='testorg', assignment_title='testassignment')


def test_run_status_missing_org_raises():
    with pytest.raises(ValueError):
        run_status(token='test', assignment_title='testassignment')


def test_run_status_missing_assignment_title_raises():
    with pytest.raises(ValueError):
        run_status(token='test', org='testorg')


def test_run_status_calls_get_all(mocker):
    mocker.patch('stoplight.repo.AssignmentRepo.get_all', return_value=None)
    run_status(token='test', org='testorg', assignment_title='testassignment')
    AssignmentRepo.get_all.assert_called()
