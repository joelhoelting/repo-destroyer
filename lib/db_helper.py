import csv
import json
import os.path


class DBHelper:
    def __init__(self, filename):
        self.filename = filename

    def read_repositories(self):
        with open('friends.json', 'r') as file:
            file_contents = json.load(file)

        print(file_contents)

        cars = [
            {'make': 'Ford', 'model': 'Fiesta'},
            {'make': 'Ford', 'model': 'Focus'}
        ]
        with open('cars.json', 'w') as file:
            json.dump(cars, file)
        pass

    # credential_file_exists = os.path.exists(self.credentials_filepath)
    # return credential_file_exists

    def read_credentials(self):
        if not os.path.exists(self.filename):
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
