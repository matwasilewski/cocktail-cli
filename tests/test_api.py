import pytest
import requests
import json

from src.cocktail_cli.api import (
    cocktails_with_ingredient,
    cocktail_components,
    cocktail_components_from_id,
    get_cocktails_that_have_given_ingredients,
    get_cocktail2ingredients,
)

cocktail_url = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=11007"


@pytest.fixture
def anis_mock(requests_mock):
    with open("resources/anis.json") as f:
        outcome = json.load(f)

    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Anis",
        json=outcome,
    )
    return requests_mock


@pytest.fixture
def blackberry_brandy_mock(requests_mock):
    with open("resources/blackberry_brandy.json") as f:
        outcome = json.load(f)

    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Blackberry brandy",
        json=outcome,
    )
    return requests_mock

@pytest.fixture
def allegheny_mock(requests_mock):
    with open("resources/allegheny.json") as f:
        outcome = json.load(f)

    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/lookup.php\?i\=11021",
        json=outcome,
    )
    return requests_mock

@pytest.fixture
def jelly_bean_mock(requests_mock):
    with open("resources/turf_cocktail.json") as f:
        outcome = json.load(f)

    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/lookup.php\?i\=12418",
        json=outcome,
    )
    return requests_mock

@pytest.fixture
def jelly_bean_mock(requests_mock):
    with open("resources/jelly_bean.json") as f:
        outcome = json.load(f)

    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/lookup.php\?i\=13775",
        json=outcome,
    )
    return requests_mock


@pytest.fixture
def margarita_mock(requests_mock):
    with open("resources/margarita.json") as f:
        outcome = json.load(f)
    requests_mock.get(
        cocktail_url,
        json=outcome,
    )
    return requests_mock


def test_cocktails_from_ingredients_1(anis_mock):
    ingredient = "Anis"
    cocktails_list = cocktails_with_ingredient(ingredient=ingredient)
    assert len(cocktails_list) == 2


def test_cocktail_details(margarita_mock):
    components_list = cocktail_components(cocktail_url=cocktail_url)
    assert len(components_list) == 4
    assert components_list[0] == "Lime juice"
    assert components_list[1] == "Salt"
    assert components_list[2] == "Tequila"
    assert components_list[3] == "Triple sec"


def test_cocktail_details_from_id(margarita_mock):
    components_list = cocktail_components_from_id("11007")
    assert len(components_list) == 4
    assert components_list[0] == "Lime juice"
    assert components_list[1] == "Salt"
    assert components_list[2] == "Tequila"
    assert components_list[3] == "Triple sec"


def test_get_cocktails_that_have_given_ingredients(
    anis_mock, blackberry_brandy_mock
):
    ingredients = ["Blackberry brandy", "Anis"]
    cocktails = get_cocktails_that_have_given_ingredients(ingredients)
    assert len(cocktails) == 4
    assert cocktails[0] == "11021"
    assert cocktails[1] == "12418"
    assert cocktails[2] == "13775"
    assert cocktails[3] == "16250"


def test_get_cocktails_that_have_given_ingredients():
    cocktail_ids = ["11021", "12418", "13775", "16250"]

    cocktail2ingredients = get_cocktail2ingredients(cocktail_ids)

    assert len(cocktail2ingredients) == 4

    assert cocktail2ingredients["11021"] == ["Blackberry brandy", "Bourbon", ]
    assert cocktail2ingredients["12418"] =
    assert cocktail2ingredients["13775"] =
    assert cocktail2ingredients["16250"] =
