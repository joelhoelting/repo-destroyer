import click
from typing import List

from .request_helper import RequestHelper
from .db_helper import DBHelper

from helpers.url_builder import build_url


class Repository:
    all = []
    db_filepath = 'db/repositories.txt'

    def __init__(self, name: str = None):
        self.name = name

    @classmethod
    def repositories_db_exists(cls):
        db_helper = DBHelper()
        db_repositories = db_helper.read_repositories()
        if db_repositories:
            cls.all = db_repositories
            return True
        return False

    @classmethod
    def update_repositories(cls, username, token) -> bool:
        request_helper = RequestHelper(url=build_url('list_repos', username=username), token=token)
        fetched_repositories = request_helper.fetch_repos()

        if fetched_repositories:
            db_helper = DBHelper()
            db_helper.write_repositories(Repository.parse_repositories(fetched_repositories))
            return cls.repositories_db_exists()  # Returns true or false
        return False

    @staticmethod
    def parse_repositories(repo_array) -> List[str]:
        new_array = [repo["name"] + "\n" for repo in repo_array]
        return new_array
