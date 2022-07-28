import requests

from src.cocktail_cli.api import cocktails_with_ingredients


def test_cocktails_from_ingredients_1():
    cocktails_list = cocktails_with_ingredients(ingredients=["vodka", "tonic", "Anis"])
    assert len(cocktails_list) == 2