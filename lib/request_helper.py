import click
import requests
import re
import time

from rich.console import Console


class RequestHelper:
    def __init__(self, url: str, method: str = "get", data: dict = None, token: str = None,
                 rate_limit_verbose: bool = False):
        self.url = url
        self.method = method
        self.data = data
        self.token = token
        self.response = None
        self.rate_limit_verbose = rate_limit_verbose
        self.requests_limit = None
        self.requests_remaining = None
        self.requests_used = None
        self.requests_reset = None

    def make_request(self):
        try:
            headers = self.set_headers()
            self.response = requests.request(method=self.method, url=self.url, headers=headers)
            self.update_rate_limit_info()

            if self.rate_limit_verbose:
                self.display_rate_limit_info()

            return self.response
        except requests.exceptions.RequestException as e:
            raise SystemExit('Please check your connection:', e)

    def request_to_json(self):
        return self.response.json()

    def fetch_repos(self):
        next_page = 1
        repositories = []

        console = Console()
        headers = self.set_headers()

        with console.status("[bold green]Fetching repositories from github..."):
            self.response = requests.request(self.method, url=self.url, headers=headers)
            self.update_rate_limit_info()
            repositories.extend(self.response.json())
            console.log(f"Success - Fetched Repositories (1 - {len(repositories)})")

        if 'link' in self.response.headers:
            next_page += 1
            link_header = self.response.headers['link']
            last_page = int(re.findall(r'&page=(\d+)>; rel="last"', link_header)[0])
            with console.status(f"[bold green]Fetching additional repositories..."):
                while next_page <= last_page:
                    next_url = self.url + f"&page={next_page}"
                    next_response = requests.request(self.method, url=next_url, headers=headers)
                    self.update_rate_limit_info()
                    next_repo_array = next_response.json()
                    repositories.extend(next_response.json())

                    starting_repo_index = (next_page - 1) * 100
                    completed_range = f"({starting_repo_index} - {starting_repo_index + len(next_repo_array)})"
                    time.sleep(.2)
                    console.log(f"Success - Fetched Repositories {completed_range}")
                    next_page += 1

            if self.rate_limit_verbose:
                self.display_rate_limit_info()

        return repositories

    def set_headers(self):
        return {'Authorization': f"Bearer {self.token}"} if self.token else None

    def update_rate_limit_info(self):
        self.requests_limit = self.response.headers['X-Ratelimit-Limit']
        self.requests_remaining = self.response.headers['X-Ratelimit-Remaining']
        self.requests_used = self.response.headers['X-Ratelimit-Used']
        self.requests_reset = int(self.response.headers['X-Ratelimit-Reset'])

    def display_rate_limit_info(self):
        local_time_reset = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.requests_reset))
        rate_limit_info = f"Request limit: {self.requests_limit}\n" \
                          f"Remaining requests: {self.requests_remaining}\n" \
                          f"Requests used: {self.requests_used}\n" \
                          f"Rate limit resets on: {local_time_reset}\n"

        click.echo(rate_limit_info)
