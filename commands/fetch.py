import click

from lib.credentials import Credentials
from lib.repository import Repository


@click.command()
def fetch():
    """Fetch a list of a repos from Github """
    credentials = Credentials()
    if not credentials.validate_credentials():
        raise click.ClickException("Invalid credentials. Run 'repo_destroyer authenticate' to update credentials.")

    if not Repository.check_repositories_db():
        click.echo("db/repositories.txt is empty or doesn't exist\n")
    else:
        click.echo(click.style("Warning: This operation will replace the contents of db/repositories.txt\n", fg="red"))

    if click.confirm('Fetch a list of your repositories from the Github API?'):
        Repository.update_repositories(username=credentials.username, token=credentials.personal_access_token)
