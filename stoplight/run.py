from typing import Optional
import typer
from rich.console import Console
from rich.table import Table

from stoplight import rc
from stoplight.repo import AssignmentRepo

app = typer.Typer()


TOKEN_OPTION_NAME = '--token'
TOKEN_OPTION = typer.Option(None, TOKEN_OPTION_NAME,
                            help='GitHub personal access token')
ORG_OPTION_NAME = '--org'
ORG_OPTION = typer.Option(
    None, ORG_OPTION_NAME,
    help='Name of GitHub organization that contains GitHub Classroom assignment repositories')
ASSIGNMENT_TITLE_OPTION_NAME = '--assignment-title'
ASSIGNMENT_TITLE_OPTION = typer.Option(
    None, ASSIGNMENT_TITLE_OPTION_NAME, help='Title of GitHub Classroom assignment')


@app.command()
def red(token: str = TOKEN_OPTION,
        org: str = ORG_OPTION,
        assignment_title: str = ASSIGNMENT_TITLE_OPTION) -> None:
    """
    Call function to disable push access to all assignment repositories.
    """
    token, org, assignment_title = fill_options(token, org, assignment_title)
    run_red(token, org, assignment_title)


def run_red(token: str, org: str, assignment_title: str):
    """
    Disable push access to all assignment repositories.
    """
    repos = AssignmentRepo.get_all(token, org, assignment_title)
    with typer.progressbar(repos, label="Updating Permissions") as progress:
        for repo in progress:
            repo.disable_student_push()
    run_status(repos=repos)


@app.command()
def green(token: str = TOKEN_OPTION,
          org: str = ORG_OPTION,
          assignment_title: str = ASSIGNMENT_TITLE_OPTION,
          all_students: bool = typer.Option(
              False, '--all', help='Enable push access to all assignment repositories.'),
          students: Optional[list[str]] = typer.Argument(None,
                                                         help='Usernames of students to enable access for')) -> None:
    """
    Enable push access to assignment repositories.
    """
    token, org, assignment_title = fill_options(token, org, assignment_title)
    if not all_students and not students:
        typer.echo(
            'Must specify --all or at least one student', err=True)
        raise typer.Exit(code=1)
    run_green(token, org, assignment_title, all_students, students)


def run_green(token: str, org: str, assignment_title: str, all_students: bool, students: list[str] = None):
    """
    Enable push access to assignment repositories.
    """
    repos = []
    if all_students:
        repos = AssignmentRepo.get_all(token, org, assignment_title)
    elif students:
        for student in students:
            repo = AssignmentRepo.get(token, org, assignment_title, student)
            if repo is None:
                typer.echo(
                    f'Skipping "{student}"... Assignment repository not found.')
            else:
                repos.append(repo)
    if repos:
        with typer.progressbar(repos, label="Updating Permissions") as progress:
            for repo in progress:
                repo.enable_student_push()  # type: ignore
        run_status(repos=repos)


@app.command()
def status(token: str = TOKEN_OPTION,
           org: str = ORG_OPTION,
           assignment_title: str = ASSIGNMENT_TITLE_OPTION):
    """
    Call function to list user permission for each assignment_title repository.
    """
    token, org, assignment_title = fill_options(token, org, assignment_title)
    run_status(token, org, assignment_title)


def run_status(token: str = None, org: str = None, assignment_title: str = None, repos=None):
    """
    List user permission for each assignment_title repository.
    """
    if repos is None:
        if token and org and assignment_title:
            repos = AssignmentRepo.get_all(token, org, assignment_title)
        else:
            raise ValueError(
                'Missing token, org, or assignment title in run_status()')
    if repos:
        table = Table(title=repos[0].assignment_title)
        table.add_column('Repo')
        table.add_column('User')
        table.add_column('Permission')
        with typer.progressbar(repos, label="Checking Status") as progress:
            for repo in progress:
                table.add_row(repo.name, repo.student(),
                              repo.student_permission())
        Console().print(table)
    else:
        typer.echo('No repositories to display--is the configuration correct?')


def fill_options(token: str, org: str, assignment_title: str) -> tuple[str, str, str]:
    """
    Fill missing options from configuration file.
    """
    rc.load()
    if token is None:
        token = rc.get('token')
    if org is None:
        org = rc.get('org')
    if assignment_title is None:
        assignment_title = rc.get('assignment_title')
    exit_if_missing(token, org, assignment_title)
    return token, org, assignment_title


def exit_if_missing(token: str, org: str, assignment_title: str):
    """
    Exit CLI program if missing any required values.
    """
    if token is None:
        typer.echo(
            f'Must specify token key in .stoplightrc or with {TOKEN_OPTION_NAME} option', err=True)
        raise typer.Exit(code=1)

    if org is None:
        typer.echo(
            f'Must specify org key in .stoplightrc or with {ORG_OPTION_NAME} option', err=True)
        raise typer.Exit(code=1)

    if assignment_title is None:
        typer.echo(
            f'Must specify assignment_title key in .stoplightrc or with {ASSIGNMENT_TITLE_OPTION_NAME} option', err=True)
        raise typer.Exit(code=1)
