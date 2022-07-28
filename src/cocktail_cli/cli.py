import os.path
from typing import List

import click

from cocktail_cli.api import (
    get_cocktails_that_have_given_ingredients,
    get_cocktail2ingredients,
    what_cocktail_can_i_make,
)


@click.command()
@click.argument("components_path")
def cli(components_path: str):
    if not os.path.isfile(components_path):
        raise FileNotFoundError(
            f"Path to ingredients {components_path} does not exist!"
        )

    with open(components_path) as f:
        ingredients = f.read().split(",")

    if len(cocktails) == 0:
        click.echo(f"We can't make any cocktails with: {ingredients}!")
    else:

        click.echo(f"With {ingredients}, we can make:")
        for cocktail in cocktails:
            click.echo(cocktail)
