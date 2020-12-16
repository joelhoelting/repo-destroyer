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
        if credentials:
            self.username = credentials[0]
            self.personal_access_token = credentials[1]

            # check if token is valid
            request_helper = RequestHelper(url=url_dict['validate'], token=self.personal_access_token)
            response = request_helper.request_to_json()
            print('hello')

            self.prompt_user_for_credentials()
        else:
            self.prompt_user_for_credentials(credentials_invalid=True)

    @staticmethod
    def credentials_db_exists(self) -> bool:
        credential_file_exists = os.path.exists(Credentials.db_filepath)
        return credential_file_exists

    @staticmethod
    def prompt_user_for_credentials(credentials_invalid: bool = False) -> None:
        if credentials_invalid:
            click.echo("Credentials are invalid or do not exist.")

        prompt = "Would you like to add/edit credentials?"
        if click.confirm(prompt):
            username = click.prompt('Username')
            personal_access_token = click.prompt('Personal Access Token')
            db_helper = DBHelper()
            db_helper.write_credentials(username, personal_access_token)
