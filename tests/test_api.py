import requests

from src.cocktail_cli.api import cocktails_from_ingredients


def test_cocktails_from_ingredients_1():
    cocktails_list = cocktails_from_ingredients(ingredients=["vodka", "tomato juice", "worcestershire sauce"])
    assert cocktails_list.status_code == 200

