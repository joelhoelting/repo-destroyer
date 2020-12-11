import click
from lib.repository import Repository


@click.command()
@click.option('-s', '--single', 'single')
def destroy(single):
    """Deletes single or multiple repositories"""
    if single:
        print(single)
        repo = Repository('x', 'y')

    # Destroy all repos
    else:
        Repository().test_method()
