import click
import os.path
import csv

from lib.credentials import Credentials
from data.url_map import url_dict


# os.path.isfile(file_path)


@click.command()
def authenticate():
    """Add or update credentials"""
    credentials = Credentials()
    credentials.read_credentials()
