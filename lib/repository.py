from typing import List

from .request_helper import RequestHelper
from .db_helper import DBHelper

from helpers.url_builder import build_url


class Repository:
    all = []

    def __init__(self, name: str = None, db_line: int = None):
        self.name = name

    def delete_self(self, username, token):
        request_helper = RequestHelper(url=build_url('delete_repo', username=username, repository=self.name),
                                       method='delete',
                                       token=token,
                                       rate_limit_verbose=True)
        response = request_helper.make_request()
        if response.status_code == 204:
            DBHelper.delete_repository(self.name)
            return True
        else:
            return False

    @classmethod
    def destroy_all(cls):
        for repo in cls.all:
            print(repo)

    @classmethod
    def check_repositories_db(cls):
        db_repositories = DBHelper.read_repositories()
        if db_repositories:
            cls.all = db_repositories
            return True
        return False

    @classmethod
    def update_repositories(cls, username, token) -> bool:
        request_helper = RequestHelper(url=build_url('list_repos', username=username), token=token,
                                       rate_limit_verbose=True)
        fetched_repositories = request_helper.fetch_repos()

        if fetched_repositories:
            DBHelper.write_repositories(Repository.parse_repositories(fetched_repositories))
            return cls.check_repositories_db()  # Returns true or false
        return False

    @staticmethod
    def parse_repositories(repo_array) -> List[str]:
        new_array = [repo["name"] + "\n" for repo in repo_array]
        return new_array
