from __future__ import annotations  # Enable type hinting
import requests


class AssignmentRepo:

    API_URL = 'https://api.github.com'
    DEFAULT_ACCEPT = 'application/vnd.github.v3+json'

    def __init__(self, token: str, org: str, name: str, assignment_title: str) -> None:
        self.org = org
        self.name = name
        self.assignment_title = assignment_title
        self.token = token
        self.header = AssignmentRepo.header(token)

    def full_name(self) -> str:
        """
        Return full name of repository.
        """
        return f'{self.org}/{self.name}'

    def student(self) -> str:
        """
        Return username of student.
        """
        return self.name.split(self.assignment_title)[1][1:]

    def student_permission(self) -> str | None:
        """
        Get repository permission for student. Return None if student is not collaborator.
        """
        r = requests.get(
            f'{AssignmentRepo.API_URL}/repos/{self.org}/{self.name}/collaborators/{self.student()}/permission',
            headers=self.header)
        if r.status_code == 404:
            return None
        return r.json()['permission']

    def disable_student_push(self) -> None:
        """
        Take away students's push access to repository by removing them as a collaborator and adding them as a collaborator with pull permission.
        """

    def enable_student_push(self) -> None:
        """
        Give user push access to repository by adding them as a collaborator with push permission.
        """

    @staticmethod
    def header(token: str) -> dict[str, str]:
        return {'Authorization': f'token {token}',
                'Accept': f'{AssignmentRepo.DEFAULT_ACCEPT}'}

    @staticmethod
    def get(token: str, org: str, assignment_title: str, student: str) -> AssignmentRepo | None:
        """
        Return assignment repository, if found. If not found, return None.
        """
        repo_name = f'{assignment_title}-{student}'
        r = requests.get(
            f'{AssignmentRepo.API_URL}/repos/{org}/{repo_name}', headers=AssignmentRepo.header(token))
        if r.status_code == 200:
            return AssignmentRepo(
                token=token,
                org=org,
                name=repo_name,
                assignment_title=assignment_title)
        return None

    @staticmethod
    def get_all(token: str, org: str, assignment_title: str) -> list[AssignmentRepo]:
        """
        Search organization and return list of assignment repositories.
        Ignore any repositories that end with 'starter' or 'solution' or that equal the assignment.
        """
        # Quotes for exact match
        # Hyphen to exclude other assignments that start with assignment
        # E.g. Assignment title 'progress-update-1' will not match 'progress-update-10'
        assignment_q = f'"{assignment_title}-"'
        r = requests.get(
            f'{AssignmentRepo.API_URL}/search/repositories',
            headers=AssignmentRepo.header(token),
            params={'q': f'{assignment_q} org:{org}'}
        )
        repos = []
        for repo in r.json()['items']:
            name = repo['name']
            if not (name == assignment_title or
                    name.endswith('starter') or
                    name.endswith('solution')):
                repos.append(AssignmentRepo(
                    token=token,
                    org=org,
                    name=name,
                    assignment_title=assignment_title))
        return repos