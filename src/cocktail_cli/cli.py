from typing import List

import click


@click.command()
@click.argument('components')
def cli(components: List[str]):
    click.echo(f'Components are: {components}!')
