from typing import List

from chalice import Chalice, Response
from github import Github, Gist, InputFileContent
import os


app = Chalice(app_name='listRepositories')
github_client = Github(os.environ['ACCESS_TOKEN'])
ORGANIZATION_NAME = os.environ['ORGANIZATION_NAME']
TEAM_ID = int(os.environ['TEAM_ID'])
GIST_ID = os.environ['GIST_ID']


@app.route('/')
def index():
    content: List[str] = [
        f'[{repo.name}]({repo.clone_url})'
        for repo in github_client.get_organization(ORGANIZATION_NAME).get_team(TEAM_ID).get_repos()
    ]

    gist: Gist = github_client.get_gist(GIST_ID)
    gist.edit(files={
        'repositories.md': InputFileContent(content='  \n'.join(content))
    })

    return Response(status_code=301, body='', headers={'Location': gist.html_url})
