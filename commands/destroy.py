import click

from lib.credentials import Credentials
from lib.repository import Repository

from helpers.text_helper import green_or_red_string


@click.command()
def destroy():
    """Destroy repositories in db/repositories"""
    credentials = Credentials()
    if not credentials.validate_credentials():
        raise click.ClickException("Invalid credentials. Run 'repo_destroyer authenticate' to update credentials.")

    if not Repository.check_repositories_db():
        raise click.ClickException("Update your repository list. Run 'repo_destroyer fetch' to update repositories")

    if click.confirm('Safely delete repos in db/repositories.txt one at a time?'):
        for repository in Repository.all:
            styled_repository_text = click.style(repository, fg='bright_yellow')
            if click.confirm(f'\nWould you like to delete: {styled_repository_text} ?'):
                r = Repository(name=repository)
                repo_was_deleted = r.delete_self(username=credentials.username, token=credentials.personal_access_token)
                success_or_error_msg = green_or_red_string(repo_was_deleted, 'successfully deleted',
                                                           'could not be deleted')
                click.echo(f"Repository: {styled_repository_text} -> {success_or_error_msg}")
            else:
                skipped_deletion_text = 'Skipped deletion of repository: '
                click.echo(skipped_deletion_text + styled_repository_text)
