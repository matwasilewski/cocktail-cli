import pytest
import requests

from src.cocktail_cli.api import cocktails_with_ingredients


@pytest.fixture
def ingredients_1_mock(requests_mock):
    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=vodka&i=tonic&i=Anis",
        json={"drinks": ["drink1", "drink2"]},
    )
    return requests_mock


def test_cocktails_from_ingredients_1(ingredients_1_mock):
    ingredients = ["vodka", "tonic", "Anis"]
    cocktails_list = cocktails_with_ingredients(ingredients=ingredients)
    assert len(cocktails_list) == 2
