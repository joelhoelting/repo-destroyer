import csv
import os.path

from typing import List, Tuple


class DBHelper:
    credentials_filepath = 'db/credentials.csv'
    repositories_filepath = 'db/repositories.txt'

    @classmethod
    def write_repositories(cls, repo_array):
        with open(cls.repositories_filepath, 'w') as f:
            f.writelines(repo_array)

    @classmethod
    def delete_repository(cls, repo):
        with open(cls.repositories_filepath, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if line.strip("\n") != repo:
                    f.write(line)
            f.truncate()

    @classmethod
    def read_repositories(cls) -> List[str]:
        if cls.file_exists_and_not_empty(cls.repositories_filepath):
            with open(cls.repositories_filepath, 'r') as f:
                repo_array = [line.strip() for line in f.readlines()]
                return repo_array
        else:
            with open(cls.repositories_filepath, 'w') as f:
                pass
            return []

    @classmethod
    def read_credentials(cls) -> Tuple[str, str]:
        if cls.file_exists_and_not_empty(cls.credentials_filepath):
            with open(cls.credentials_filepath, 'r') as f:
                reader = csv.DictReader(f)
                for line in reader:
                    username, personal_access_token = line.get('username'), line.get('personal_access_token')
                    if username and personal_access_token:
                        return username, personal_access_token
        else:
            with open(cls.credentials_filepath, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=["username", "personal_access_token"])
                writer.writeheader()

    @classmethod
    def write_credentials(cls, username: str, personal_access_token: str) -> None:
        with open(cls.credentials_filepath, "w") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "personal_access_token"])
            writer.writeheader()
            writer.writerow({"username": username, "personal_access_token": personal_access_token})

    @staticmethod
    def file_exists_and_not_empty(filepath: str) -> bool:
        return os.path.exists(filepath) and os.stat(filepath).st_size > 0
