import click
import requests
import re
import time

from rich.console import Console

from .db_helper import DBHelper


class RequestHelper:
    def __init__(self, url: str, method: str = "get", data: dict = None, token: str = None):
        self.url = url
        self.method = method
        self.data = data
        self.token = token

    def request_to_json(self):
        try:
            headers = self.set_headers()
            response = requests.request(method=self.method, url=self.url, headers=headers)
            response_to_json = response.json()
            return response, response_to_json
        except requests.exceptions.RequestException as e:
            raise SystemExit('Please check your connection:', e)

    def fetch_repos(self):
        next_page = 1
        repositories = []

        console = Console()
        headers = self.set_headers()

        with console.status("[bold green]Fetching repositories from github..."):
            response = requests.request(self.method, url=self.url, headers=headers)
            repositories.extend(response.json())
            console.log(f"Success - Fetched Repositories (1 - {len(repositories)})")

        if 'link' in response.headers:
            next_page += 1
            link_header = response.headers['link']
            last_page = int(re.findall(r'&page=(\d+)>; rel="last"', link_header)[0])
            with console.status(f"[bold green]Fetching additional repositories..."):
                while next_page <= last_page:
                    next_url = self.url + f"&page={next_page}"
                    next_response = requests.request(self.method, url=next_url, headers=headers)
                    next_repo_array = next_response.json()
                    repositories.extend(next_repo_array)

                    repo_requests_limit = next_response.headers['X-Ratelimit-Limit']
                    repo_requests_remaining = next_response.headers['X-Ratelimit-Remaining']
                    repo_requests_used = next_response.headers['X-Ratelimit-Used']
                    repo_requests_reset = int(next_response.headers['X-Ratelimit-Reset'])
                    local_time_reset = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(repo_requests_reset))

                    starting_repo_index = (next_page - 1) * 100
                    completed_range = f"({starting_repo_index} - {starting_repo_index + len(next_repo_array)})"
                    time.sleep(1)
                    console.log(f"Success - Fetched Repositories {completed_range}")
                    next_page += 1

            rate_limit_info = f"Request limit: {repo_requests_limit}\n" \
                              f"Remaining requests: {repo_requests_remaining}\n" \
                              f"Requests used: {repo_requests_used}\n" \
                              f"Rate limit resets on: {local_time_reset}\n"

            click.echo(rate_limit_info)

        return repositories

    def set_headers(self):
        return {'Authorization': f"Bearer {self.token}"} if self.token else None
