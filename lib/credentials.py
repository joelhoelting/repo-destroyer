import click

from .db_helper import DBHelper
from .request_helper import RequestHelper

from helpers.url_builder import build_url
from helpers.text_helper import green_or_red_string

from typing import TypeVar

CredentialsType = TypeVar("CredentialsType", bound="Credentials")


class Credentials:
    def __init__(self) -> None:
        self.username = None
        self.personal_access_token = None
        self.username_valid = False
        self.personal_access_token_valid = False

    def validate_username(self) -> bool:
        username_request_helper = RequestHelper(url=build_url('validate_user', username=self.username))
        username_request_helper.make_request()
        return username_request_helper.response.status_code == 200

    def validate_personal_access_token(self) -> bool:
        token_request_helper = RequestHelper(url=build_url('validate_token'), token=self.personal_access_token)
        token_request_helper.make_request()
        return token_request_helper.response.status_code == 200

    def validate_credentials(self) -> CredentialsType:
        credentials = DBHelper.read_credentials()
        if credentials:
            self.username = credentials[0]
            self.personal_access_token = credentials[1]

            # check if username is valid
            self.username_valid = self.validate_username()

            # check if token is valid
            self.personal_access_token_valid = self.validate_personal_access_token()

            if self.username_valid and self.personal_access_token_valid:
                return True

        return False

    def display_token_info(self):
        curr_username_str = self.username or '<empty>'
        curr_token_str = self.personal_access_token or '<empty>'
        username_valid_str = green_or_red_string(self.username_valid, 'valid', 'invalid')
        personal_access_token_valid_str = green_or_red_string(self.personal_access_token_valid, 'valid', 'invalid')

        click.echo(f"Github username: {curr_username_str} ({username_valid_str})")
        click.echo(f"Github token: {curr_token_str} ({personal_access_token_valid_str})\n")

        if not self.personal_access_token_valid:
            click.echo("1. Visit https://github.com/settings/tokens and create a token with 'delete_repo' scope.")
            click.echo("2. Provide your username and token in the prompt below: \n")

    def prompt_user_for_credentials(self) -> None:
        prompt = "Update github credentials?"
        if click.confirm(prompt):
            self.username = click.prompt('Username')
            if not self.validate_username():
                return click.echo(click.style('username is invalid. Please try again.', fg='red'))
            self.personal_access_token = click.prompt('Personal Access Token')
            if not self.validate_personal_access_token():
                return click.echo(click.style('token is invalid. Please try again.', fg='red'))

            DBHelper.write_credentials(self.username, self.personal_access_token)
