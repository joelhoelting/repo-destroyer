import click
import os.path

from .db_helper import DBHelper
from .request_helper import RequestHelper

from data.url_map import url_dict


class Credentials:
    db_filepath = 'db/credentials.csv'

    def __init__(self) -> None:
        self.username = None
        self.personal_access_token = None

    def display_credentials(self) -> None:
        printed_credentials = f"Current credentials ({self.db_filepath}):\n\n" \
                              f"Username: {self.username}\n" \
                              f"Personal Access Token: {self.personal_access_token}" \
                              f"\n"

        click.echo(printed_credentials)

    def read_credentials(self) -> None:
        credentials = DBHelper().read_credentials()
        credentials_valid = False
        if credentials:
            self.username = credentials[0]
            self.personal_access_token = credentials[1]

            # check if token is valid
            request_helper = RequestHelper(url=url_dict['validate'], token=self.personal_access_token)
            response, json = request_helper.request_to_json()

            credentials_valid = response.status_code == 200

        message = "valid\n" if credentials_valid else "invalid\n"
        message_color = "green" if credentials_valid else "red"
        click.echo(f"Github token status: " + click.style(message, fg=message_color))

        if not credentials_valid:
            click.echo("1. Visit https://github.com/settings/tokens and create a token with 'delete_repo scope'.")
            click.echo("2. Provide your username and token in the prompt below: \n")
        self.prompt_user_for_credentials()

    @staticmethod
    def credentials_db_exists(self) -> bool:
        credential_file_exists = os.path.exists(Credentials.db_filepath)
        return credential_file_exists

    @staticmethod
    def prompt_user_for_credentials() -> None:
        prompt = "Update credentials?"
        if click.confirm(prompt):
            username = click.prompt('Username')
            personal_access_token = click.prompt('Personal Access Token')
            db_helper = DBHelper()
            db_helper.write_credentials(username, personal_access_token)
