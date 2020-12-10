import requests


class Repository:
    repositories = []

    def __init__(self, name, url):
        self.slug = name
        self.url = url

    @classmethod
    def update_repositories(cls, repositories):
        if not cls.repositories:
            cls.repositories.append('twenty')
        else:
            print('list is full')

    @classmethod
    def delete_all(cls):
        if not cls.repositories:
            repos = requests.get('https://api.github.com/users/joelhoelting/repos?per_page=2000')
            repos_json = repos.json()

            for repo in repos_json:
                print(repo["name"])
            # cls.update_repositories(repositories)
        print(cls.repositories)
