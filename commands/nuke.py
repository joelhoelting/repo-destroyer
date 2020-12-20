import click


@click.command()
@click.option('-i', '--iterate', 'iterate', help='Delete repos one by one', is_flag=True)
def nuke(iterate):
    """Destroy repositories in db/repositories"""
    pass
    # repository_arr =
