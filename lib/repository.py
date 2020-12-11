from .db_helper import DBHelper


class Repository:
    all = []

    def __init__(self, name: str = None, url: str = None):
        self.slug = name
        self.url = url
        Repository.update_repositories()

    @classmethod
    def test_method(cls):
        print('hello world')

    @classmethod
    def update_repositories(cls):
        if not cls.all:

            cls.all.append('twenty')
        else:
            print('list is full')

    @classmethod
    def delete_all(cls):
        pass
        # if not cls.repositories:
        #     repos = requests.get('https://api.github.com/users/joelhoelting/repos?per_page=2000')
        #     repos_json = repos.json()
        #
        #     for repo in repos_json:
        #         print(repo["name"])
        # cls.update_repositories(repositories)
