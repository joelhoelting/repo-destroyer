import click
import os.path
import csv

from lib.credentials import Credentials


# os.path.isfile(file_path)


@click.command()
def authenticate():
    """Add or update credentials"""
    credentials = Credentials()
    credentials.validate_credentials()
    credentials.display_token_info()

    credentials.prompt_user_for_credentials()
