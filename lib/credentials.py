import click
import os.path

from .csv_helper import CSVHelper


class Credentials:
    def __init__(self, credentials_filepath: str = 'db/credentials.csv') -> None:
        self.credentials_filepath = credentials_filepath
        self.username = None
        self.personal_access_token = None

    def credentials_db_exists(self) -> bool:
        credential_file_exists = os.path.exists(self.credentials_filepath)
        return credential_file_exists

    def display_credentials(self) -> None:
        printed_credentials = f"Current credentials:\n\n" \
                              f"Username: {self.username}\n" \
                              f"Personal Access Token: {self.personal_access_token}" \
                              f"\n"

        click.echo(printed_credentials)

    def prompt_user_for_credentials(self, credentials_invalid: bool = False) -> None:
        if credentials_invalid:
            click.echo("Credentials are invalid or do not exist.")

        prompt = "Would you like to add/edit credentials?"
        if click.confirm(prompt):
            username = click.prompt('Username')
            personal_access_token = click.prompt('Personal Access Token')
            csv_helper = CSVHelper(self.credentials_filepath)
            csv_helper.write_credentials(username, personal_access_token)

    def read_credentials(self) -> None:
        if self.credentials_db_exists():
            credentials = CSVHelper(self.credentials_filepath).read_credentials()
            if credentials:
                self.username = credentials[0]
                self.personal_access_token = credentials[1]
                self.display_credentials()
            else:
                self.prompt_user_for_credentials(credentials_invalid=True)
        else:
            self.prompt_user_for_credentials()
