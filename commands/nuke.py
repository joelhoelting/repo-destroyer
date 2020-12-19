import click


@click.command()
@click.option('-i', '--iterate', 'iterate', help='Delete repos one at a time ', is_flag=True)
def nuke(iterate):
    """Destroy all repositories after giving permission"""
   