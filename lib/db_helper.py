import csv
import os.path

from typing import List, Tuple


class DBHelper:
    credentials_filepath = 'db/credentials.csv'
    repositories_filepath = 'db/repositories.txt'

    def write_repositories(self, repo_array):
        with open(self.repositories_filepath, 'w') as f:
            f.writelines(repo_array)

    def read_repositories(self) -> List[str]:
        if self.file_exists_and_not_empty(self.repositories_filepath):
            with open(self.repositories_filepath, 'r') as f:
                repo_array = [line.strip() for line in f.readlines()]
                return repo_array
        else:
            return []

    def read_credentials(self) -> Tuple[str, str]:
        if self.file_exists_and_not_empty(self.credentials_filepath):
            with open(self.credentials_filepath, "r") as f:
                reader = csv.DictReader(f)
                for line in reader:
                    username, personal_access_token = line.get('username'), line.get('personal_access_token')
                    if username and personal_access_token:
                        return username, personal_access_token

    def write_credentials(self, username: str, personal_access_token: str) -> None:
        with open(self.credentials_filepath, "w") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "personal_access_token"])
            writer.writeheader()
            writer.writerow({"username": username, "personal_access_token": personal_access_token})

    @staticmethod
    def file_exists_and_not_empty(filename: str) -> bool:
        return os.path.exists(filename) and os.stat(filename).st_size > 0
