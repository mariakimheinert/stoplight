import json
import requests
import typer
from typing import List

from stoplight import rc

app = typer.Typer()


TOKEN_OPTION_NAME = '--token'
TOKEN_OPTION = typer.Option(None, TOKEN_OPTION_NAME, help = 'GitHub personal access token')
ORG_OPTION_NAME = '--org'
ORG_OPTION = typer.Option(None, ORG_OPTION_NAME, help = 'Name of GitHub organization that contains GitHub Classroom assignment repositories')
ASSIGNMENT_OPTION_NAME = '--assignment'
ASSIGNMENT_OPTION = typer.Option(None, ASSIGNMENT_OPTION_NAME, help = 'Name of GitHub Classroom assignment')


@app.command()
def red(token: str = TOKEN_OPTION,
        org: str = ORG_OPTION,
        assignment: str = ASSIGNMENT_OPTION):
    '''
    Disable push access to all assignment repositories.
    '''
    token, org, assignment = fill_options(token, org, assignment)
    exit_if_missing(token, org, assignment)


@app.command()
def green(token: str = TOKEN_OPTION,
        org: str = ORG_OPTION,
        assignment: str = ASSIGNMENT_OPTION,
        users: List[str] = typer.Argument(..., help = 'GitHub users to enable access for')):
    '''
    Enable push access to assignment repositories.
    '''
    token, org, assignment = fill_options(token, org, assignment)
    exit_if_missing(token, org, assignment)


def fill_options(token, org, assignment):
    '''
    Fill missing options from configuration file.
    '''
    rc.load()
    if token is None:
        token = rc.get('token')
    if org is None:
        org = rc.get('org')
    if assignment is None:
        assignment = rc.get('assignment')
    return token, org, assignment


def exit_if_missing(token: str, org: str, assignment: str):
    '''
    Exit CLI program if missing any required values.
    '''
    if token is None:
        typer.echo(f'Must specify token key in .stoplightrc or with {TOKEN_OPTION_NAME} option', err = True)
        raise typer.Exit(code = 1)
    
    if org is None:
        typer.echo(f'Must specify org key in .stoplightrc or with {ORG_OPTION_NAME} option', err = True)
        raise typer.Exit(code = 1)
    
    if assignment is None:
        typer.echo(f'Must specify assignment key in .stoplightrc or with {ASSIGNMENT_OPTION_NAME} option', err = True)
        raise typer.Exit(code = 1)


def generate_headers(token, accept):
    """Generate headers to be used in requests."""
    return {"Authorization": f'token {token}', "Accept": accept}


# def run():
#     config = parse_config()
#     token = config["token"]
#     api = "https://api.github.com"
#     accept = "application/vnd.github.v3+json"
#     headers = generate_headers(token, accept)

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


