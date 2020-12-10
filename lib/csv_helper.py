import csv


class CSVHelper:
    def __init__(self, filename):
        self.filename = filename

    def read_credentials(self):
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
