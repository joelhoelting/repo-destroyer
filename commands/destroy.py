import click

from lib.repository import Repository


@click.command()
@click.option('-r', '--repo', 'repository')
@click.option('-s', '--safe', 'safe', is_flag=True)
def destroy(repository, safe):
    """Deletes single or multiple repositories"""
    if not Repository.repositories_db_exists():
        Repository.update_repositories()
    if repository:
        repo = Repository('x', 'y')

    elif safe:
        print('safe')
    # Destroy all repos
    else:
        Repository.check_repositories_db() or Repository.update_repositories()
