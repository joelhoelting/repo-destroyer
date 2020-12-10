import click
import os.path
import csv

from lib.credentials import Credentials


# os.path.isfile(file_path)


@click.command()
def authenticate():
    """Add or update credentials"""
    credentials = Credentials()
    credentials.read_credentials()
