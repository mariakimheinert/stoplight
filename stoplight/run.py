import json
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
    None, ORG_OPTION_NAME, help='Name of GitHub organization that contains GitHub Classroom assignment repositories')
ASSIGNMENT_TITLE_OPTION_NAME = '--assignment-title'
ASSIGNMENT_TITLE_OPTION = typer.Option(
    None, ASSIGNMENT_TITLE_OPTION_NAME, help='Title of GitHub Classroom assignment')


@app.command()
def red(token: str = TOKEN_OPTION,
        org: str = ORG_OPTION,
        assignment_title: str = ASSIGNMENT_TITLE_OPTION) -> None:
    """
    Call function to disable push access to all assignment_title repositories.
    """
    token, org, assignment_title = fill_options(token, org, assignment_title)
    run_red(token, org, assignment_title)


def run_red(token: str, org: str, assignment_title: str):
    """
    Disable push access to all assignment_title repositories.
    """
    pass


@app.command()
def green(token: str = TOKEN_OPTION,
          org: str = ORG_OPTION,
          assignment_title: str = ASSIGNMENT_TITLE_OPTION,
          users: list[str] = typer.Argument(...,
                                            help='GitHub users to enable access for')) -> None:
    """
    Enable push access to assignment_title repositories.
    """
    token, org, assignment_title = fill_options(token, org, assignment_title)


@app.command()
def status(token: str = TOKEN_OPTION,
           org: str = ORG_OPTION,
           assignment_title: str = ASSIGNMENT_TITLE_OPTION):
    """
    Call function to list user permission for each assignment_title repository.
    """
    token, org, assignment_title = fill_options(token, org, assignment_title)
    run_status(token, org, assignment_title)


def run_status(token: str, org: str, assignment_title: str):
    """
    List user permission for each assignment_title repository.
    """
    repos = AssignmentRepo.get_all(token, org, assignment_title)
    table = Table(title=assignment_title)
    table.add_column('Repo')
    table.add_column('User')
    table.add_column('Permission')
    for repo in repos:
        table.add_row(repo.name, repo.student(), repo.student_permission())
    Console().print(table)


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

    # def get_repositories():
    # def run():
    #     config = parse_config()
    #     token = config["token"]
    #     api = "https://api.github.com"
    #     accept = "application/vnd.github.v3+json"
    #     headers = compose_headers(token, accept)

    #     repos = requests.get(
    #         f"{api}/search/repositories", headers=headers, params={"q": "test org:mkhcourses"}
    #     )
    #     print(repos.json()['items'])

    #     blacklist = ['starter', 'solution']
    #     # Remove any repos that contain any words in blacklist
    #     sanitized_results = [result for result in repos.json()['items'] if not any(
    #         word in result['full_name'] for word in blacklist)]

    #     print(len(sanitized_results))
    # repos = requests.get(
    #     f'{api}/orgs/mkhcourses/repos', headers=headers)

    # print(repos)
    # print(len(repos.json()))

    # collaborators = requests.get(
    #     f'{api}/repos/{config["org"]}/test/collaborators', headers=headers)
    # print(collaborators.json())
