import pytest
import responses
from responses import matchers

from stoplight.repo import AssignmentRepo

REPO = None


@pytest.fixture(autouse=True)
def setup():
    global REPO
    REPO = AssignmentRepo(token='test', org='testorg',
                          name='testassignment-testuser', assignment_title='testassignment')
    yield


def test_full_name_returns_org_and_name():
    assert REPO.full_name() == 'testorg/testassignment-testuser'


def test_student_returns_student_username():
    assert REPO.student() == 'testuser'


def test_student_returns_username_that_contains_hyphen():
    repo = AssignmentRepo(token='test', org='testorg',
                          name='testassignment-test-user', assignment_title='testassignment')
    assert repo.student() == 'test-user'


@responses.activate
def test_get_status_200_returns_assignmentrepo():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/repos/testorg/testassignment-testuser',
        status=200)
    assert isinstance(REPO.get(
        token='test',
        org='testorg',
        assignment_title='testassignment',
        student='testuser'), AssignmentRepo)


@responses.activate
def test_get_status_301_returns_none():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/repos/testorg/testassignment-testuser',
        status=301)
    assert REPO.get(
        token='test',
        org='testorg',
        assignment_title='testassignment',
        student='testuser') is None


@responses.activate
def test_get_status_403_returns_none():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/repos/testorg/testassignment-testuser',
        status=403)
    assert REPO.get(
        token='test',
        org='testorg',
        assignment_title='testassignment',
        student='testuser') is None


@responses.activate
def test_get_status_404_returns_none():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/repos/testorg/testassignment-testuser',
        status=404)
    assert REPO.get(
        token='test',
        org='testorg',
        assignment_title='testassignment',
        student='testuser') is None


@responses.activate
def test_get_all_ignores_repo_that_equals_assignment():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/search/repositories',
        match=[matchers.query_param_matcher(
            {'q': '"testassignment-" org:testorg'})],
        json={
            'items': [
                {'name': 'testassignment-starter'},
                {'name': 'starter-testassignment'},
                {'name': 'testassignment-testuser'},
                {'name': 'testassignment'}
            ]})
    repos = AssignmentRepo.get_all(token='test',
                                   org='testorg',
                                   assignment_title='testassignment')
    assert 'testassignment' not in map(lambda repo: repo.name, repos)


@responses.activate
def test_get_all_ignores_repo_that_endswith_starter():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/search/repositories',
        match=[matchers.query_param_matcher(
            {'q': '"testassignment-" org:testorg'})],
        json={
            'items': [
                {'name': 'testassignment-starter'},
                {'name': 'starter-testassignment'},
                {'name': 'testassignment-testuser'},
            ]})
    repos = AssignmentRepo.get_all(token='test',
                                   org='testorg',
                                   assignment_title='testassignment')
    assert 'testassignment-starter' not in map(lambda repo: repo.name, repos)
    assert 'starter-testassignment' in map(lambda repo: repo.name, repos)


@responses.activate
def test_get_all_ignores_repo_that_endswith_solution():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/search/repositories',
        match=[matchers.query_param_matcher(
            {'q': '"testassignment-" org:testorg'})],
        json={
            'items': [
                {'name': 'testassignment-solution'},
                {'name': 'solution-testassignment'},
                {'name': 'testassignment-testuser'},
            ]})
    repos = AssignmentRepo.get_all(
        token='test', org='testorg',
        assignment_title='testassignment')
    assert 'testassignment-solution' not in map(lambda repo: repo.name, repos)
    assert 'solution-testassignment' in map(lambda repo: repo.name, repos)


@responses.activate
def test_get_all_returns_names():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/search/repositories',
        match=[matchers.query_param_matcher(
            {'q': '"testassignment-" org:testorg'})],
        json={
            'items': [
                {'name': 'testassignment-testuser1'},
                {'name': 'testassignment-testuser2'}
            ]})
    repos = AssignmentRepo.get_all(
        token='test', org='testorg',
        assignment_title='testassignment')
    assert 'testassignment-testuser1' in map(lambda repo: repo.name, repos)
    assert 'testassignment-testuser2' in map(lambda repo: repo.name, repos)


@responses.activate
def test_get_all_status_422_returns_empty_list():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/search/repositories',
        match=[matchers.query_param_matcher(
            {'q': '"testassignment-" org:testorg'})],
        status=422)
    repos = AssignmentRepo.get_all(
        token='test', org='testorg',
        assignment_title='testassignment')
    assert repos == []


@responses.activate
def test_student_permission_status_404_returns_none():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/repos/testorg/testassignment-testuser/collaborators/testuser/permission',
        status=404
    )
    assert REPO.student_permission() is None


@responses.activate
def test_student_permission_returns_permission():
    responses.add(
        method=responses.GET,
        url=f'{AssignmentRepo.API_URL}/repos/testorg/testassignment-testuser/collaborators/testuser/permission',
        json={
            'permission': 'write'
        }
    )
    assert REPO.student_permission() == 'write'


@responses.activate
def test_disable_student_push_request_contains_permission_pull():
    url = f'{AssignmentRepo.API_URL}/repos/testorg/testassignment-testuser/collaborators/testuser'
    responses.add(
        method=responses.PUT,
        url=url,
        match=[
            matchers.json_params_matcher({'permission': 'pull'})
        ]
    )
    REPO.disable_student_push()
    assert responses.assert_call_count(url, 1) is True


@responses.activate
def test_enable_student_push_request_contains_permission_push():
    url = f'{AssignmentRepo.API_URL}/repos/testorg/testassignment-testuser/collaborators/testuser'
    responses.add(
        method=responses.PUT,
        url=url,
        match=[
            matchers.json_params_matcher({'permission': 'push'})
        ]
    )
    REPO.enable_student_push()
    assert responses.assert_call_count(url, 1) is True
