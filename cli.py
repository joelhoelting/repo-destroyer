import click

from commands.authenticate import authenticate
from commands.destroy import destroy


@click.group()
def entry_point():
    pass


entry_point.add_command(authenticate)
entry_point.add_command(destroy)

if __name__ == '__main__':
    entry_point(['authenticate'])
