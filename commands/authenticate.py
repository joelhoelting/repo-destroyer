import click

from lib.credentials import Credentials


@click.command()
def authenticate():
    """Add or update GitHub credentials"""
    credentials = Credentials()
    credentials.validate_credentials()
    credentials.display_token_info()
    credentials.prompt_user_for_credentials()
