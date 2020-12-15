import click

from .request_helper import RequestHelper
from .db_helper import DBHelper


class Repository:
    all = []
    db_filepath = 'db/repositories.txt'

    def __init__(self, name: str = None, url: str = None):
        self.slug = name
        self.url = url

    @classmethod
    def check_repositories_db(cls):
        db_helper = DBHelper(cls.db_filepath)
        db_repositories = db_helper.read_repositories()
        if db_repositories:
            cls.all = db_repositories
            return True
        return False

    @classmethod
    def update_repositories(cls):
        click.echo("db/repositories.txt is empty or doesn't exist")
        if click.confirm('Fetch a list of your repositories from the Github API?'):
            request_helper = RequestHelper('https://api.github.com/users/joelhoelting/repos?per_page=100')
            fetched_repositories = request_helper.fetch_repos()

            db_helper = DBHelper(cls.db_filepath)
            db_helper.write_repositories(Repository.parse_repositories(fetched_repositories))
            cls.check_repositories_db()
        return False

    @staticmethod
    def parse_repositories(repo_array):
        new_array = [repo["name"] + "\n" for repo in repo_array]
        return new_array
