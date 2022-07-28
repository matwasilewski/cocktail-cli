from typing import List

import click


@click.command()
def cli(components: List[str]):
    return f"Components are: {components}"