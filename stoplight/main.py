import json
import requests


def parse_config():
    """Parse configuration file."""
    return json.load(open("config.json"))


def generate_headers(token, accept):
    """Generate headers to be used in requests."""
    return {"Authorization": f'token {token}', "Accept": accept}


config = parse_config()
token = config["token"]
api = "https://api.github.com"
accept = "application/vnd.github.v3+json"
headers = generate_headers(token, accept)

repos = requests.get(
    f"{api}/search/repositories", headers=headers, params={"q": "test org:mkhcourses"}
)
print(repos.json()['items'])

blacklist = ['starter', 'solution']
# Remove any repos that contain any words in blacklist
sanitized_results = [result for result in repos.json()['items'] if not any(
    word in result['full_name'] for word in blacklist)]

print(len(sanitized_results))
# repos = requests.get(
#     f'{api}/orgs/mkhcourses/repos', headers=headers)

# print(repos)
# print(len(repos.json()))

# collaborators = requests.get(
#     f'{api}/repos/{config["organization"]}/test/collaborators', headers=headers)
# print(collaborators.json())
