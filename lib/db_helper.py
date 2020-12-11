import csv
import json
import os.path

from typing import List


class DBHelper:
    def __init__(self, filename):
        self.filename = filename

    def file_exists_and_not_empty(self):
        return os.path.exists(self.filename) and os.stat(self.filename).st_size > 0

    def write_repositories(self, repo_array):
        with open(self.filename, 'w') as f:
            f.writelines(repo_array)

    def read_repositories(self) -> List:
        if self.file_exists_and_not_empty():
            with open(self.filename, 'r') as f:
                repo_array = [line.strip() for line in f.readlines()]
                return repo_array
        else:
            return []

    def read_credentials(self):
        if not self.file_exists_and_not_empty():
            return False

        with open(self.filename, "r") as f:
            reader = csv.DictReader(f)
            for line in reader:
                username, personal_access_token = line.get('username'), line.get('personal_access_token')
                if username and personal_access_token:
                    return (username, personal_access_token)
            else:
                return False

    def write_credentials(self, username: str, personal_access_token: str) -> None:
        with open(self.filename, "w") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "personal_access_token"])
            writer.writeheader()
            writer.writerow({"username": username, "personal_access_token": personal_access_token})
