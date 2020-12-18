import click
import os.path

from .db_helper import DBHelper
from .request_helper import RequestHelper

from helpers.url_builder import build_url
from helpers.text_helper import green_or_red_string

from typing import TypeVar

CredentialsType = TypeVar("CredentialsType", bound="Credentials")


class Credentials:
    db_filepath = 'db/credentials.csv'

    def __init__(self) -> None:
        self.username = None
        self.personal_access_token = None
        self.username_valid = False
        self.personal_access_token_valid = False

    def display_credentials(self) -> None:
        printed_credentials = f"Current credentials ({self.db_filepath}):\n\n" \
                              f"Username: {self.username}\n" \
                              f"Personal Access Token: {self.personal_access_token}" \
                              f"\n"

        click.echo(printed_credentials)

    def validate_credentials(self) -> CredentialsType:
        credentials = DBHelper().read_credentials()
        if credentials:
            self.username = credentials[0]
            self.personal_access_token = credentials[1]

            # check if username is valid
            username_request_helper = RequestHelper(url=build_url('validate_user', self.username))
            response, json = username_request_helper.request_to_json()
            self.username_valid = response.status_code == 200

            # check if token is valid
            request_helper = RequestHelper(url=build_url('validate_token'), token=self.personal_access_token)
            response, json = request_helper.request_to_json()
            self.personal_access_token_valid = response.status_code == 200

        return self

    def display_token_info(self):
        printed_credentials = f"Current credentials ({self.db_filepath}):\n\n" \
                              f"Username: {self.username or '<empty>'}\n" \
                              f"Personal Access Token: {self.personal_access_token or '<empty>'}" \
                              f"\n"

        click.echo(printed_credentials)

        username_valid_string = green_or_red_string(self.username_valid, 'valid', 'invalid')
        personal_access_token_valid_string = green_or_red_string(self.personal_access_token_valid, 'valid', 'invalid')

        click.echo(f"Github username status: " + username_valid_string)
        click.echo(f"Github personal access token status: " + personal_access_token_valid_string + "\n")

        if not self.personal_access_token_valid:
            click.echo("1. Visit https://github.com/settings/tokens and create a token with 'delete_repo' scope.")
            click.echo("2. Provide your username and token in the prompt below: \n")

    @staticmethod
    def credentials_db_exists() -> bool:
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
