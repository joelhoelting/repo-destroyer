import click

from commands.authenticate import authenticate
from commands.destroy import destroy
from commands.fetch import fetch


@click.group()
def entry_point():
    pass


entry_point.add_command(authenticate)
entry_point.add_command(destroy)
entry_point.add_command(fetch)

if __name__ == '__main__':
    entry_point(['destroy'])
