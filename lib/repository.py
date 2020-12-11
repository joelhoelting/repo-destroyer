from .request_helper import RequestHelper
from .db_helper import DBHelper


class Repository:
    all = []
    db_filepath = 'db/repositories.txt'

    def __init__(self, name: str = None, url: str = None):
        self.slug = name
        self.url = url
        Repository.update_repositories()

    @classmethod
    def update_repositories(cls):
        if not cls.all:
            db_helper = DBHelper(cls.db_filepath)
            db_repositories = db_helper.read_repositories()

            if not db_repositories:
                request_helper = RequestHelper('https://api.github.com/users/joelhoelting/repos?per_page=100')
                fetched_repositories = request_helper.request_to_json()

                db_helper.write_repositories(Repository.parse_repositories(fetched_repositories))

            cls.all = db_repositories or fetched_repositories
        else:
            print('list is full')

    @staticmethod
    def parse_repositories(repo_array):
        new_array = [repo["name"] + "\n" for repo in repo_array]
        return new_array
