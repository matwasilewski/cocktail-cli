import pytest
import requests
import json

from src.cocktail_cli.api import (
    cocktails_with_ingredients,
    cocktail_components,
)

cocktail_url = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=11007"


@pytest.fixture
def ingredients_1_mock(requests_mock):
    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=vodka&i=tonic&i=Anis",
        json={"drinks": ["drink1", "drink2"]},
    )
    return requests_mock


@pytest.fixture
def cocktail_2_mock(requests_mock):
    with open("resources/11007_drink_details.json") as f:
        outcome = json.load(f)
    requests_mock.get(
        cocktail_url,
        json=outcome,
    )
    return requests_mock


def test_cocktails_from_ingredients_1(ingredients_1_mock):
    ingredients = ["vodka", "tonic", "Anis"]
    cocktails_list = cocktails_with_ingredients(ingredients=ingredients)
    assert len(cocktails_list) == 2


def test_cocktail_details(cocktail_2_mock):
    components_list = cocktail_components(cocktail_url=cocktail_url)
    assert len(components_list) == 4
    assert components_list[0] == "Lime juice"
    assert components_list[1] == "Salt"
    assert components_list[2] == "Tequila"
    assert components_list[3] == "Triple sec"
