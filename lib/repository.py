import click

from .request_helper import RequestHelper
from .db_helper import DBHelper

from typing import List


class Repository:
    all = []
    db_filepath = 'db/repositories.txt'

    def __init__(self, name: str = None):
        self.name = name

    @classmethod
    def check_repositories_db(cls):
        db_helper = DBHelper()
        db_repositories = db_helper.read_repositories()
        if db_repositories:
            cls.all = db_repositories
            return True
        return False

    @classmethod
    def update_repositories(cls) -> bool:
        click.echo("db/repositories.txt is empty or doesn't exist")
        if click.confirm('Fetch a list of your repositories from the Github API?'):
            request_helper = RequestHelper('https://api.github.com/users/joelhoelting/repos?per_page=100')
            fetched_repositories = request_helper.fetch_repos()

            if fetched_repositories:
                db_helper = DBHelper()
                db_helper.write_repositories(Repository.parse_repositories(fetched_repositories))
                cls.check_repositories_db()  # Returns true or false
        return False

    @staticmethod
    def parse_repositories(repo_array) -> List[str]:
        new_array = [repo["name"] + "\n" for repo in repo_array]
        return new_array
