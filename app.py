from typing import List

from chalice import Chalice, Response
from github import Github, Gist, Organization, Team, InputFileContent
import os


app = Chalice(app_name='listRepositories')
github_client = Github(os.environ['ACCESS_TOKEN'])

organization: Organization.Organization = github_client.get_organization(os.environ['ORGANIZATION_NAME'])
team: Team.Team = organization.get_team(int(os.environ['TEAM_ID']))
gist: Gist.Gist = github_client.get_gist(os.environ['GIST_ID'])


@app.route('/')
def index():
    content: List[str] = [
        f'[{repo.name}]({repo.clone_url})'
        for repo in team.get_repos()
    ]

    gist.edit(files={
        'repositories.md': InputFileContent(content='  \n'.join(content)),
    })

    return Response(status_code=301, body='', headers={'Location': gist.html_url})
