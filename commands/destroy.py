import click
from lib.repository import Repository


@click.command()
@click.option('-r', '--repo', 'repository')
def destroy(repository):
    """Deletes a single repo"""
    if repository:
        repo = Repository('x', 'y', 'z')

    # Destroy all repos
    else:
        Repository.delete_all()
