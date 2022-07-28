import pytest
import requests
import json

from cocktail_cli.api import (
    cocktails_with_ingredient,
    cocktail_components,
    cocktail_components_from_id,
    get_cocktails_that_have_given_ingredients,
    get_cocktail2ingredients,
    what_cocktail_can_i_make,
    get_cocktails,
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
        "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=11021",
        json=outcome,
    )
    return requests_mock


@pytest.fixture
def jelly_bean_mock(requests_mock):
    with open("resources/jelly_bean.json") as f:
        outcome = json.load(f)

    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=13775",
        json=outcome,
    )
    return requests_mock


@pytest.fixture
def turf_cocktail_mock(requests_mock):
    with open("resources/turf_cocktail.json") as f:
        outcome = json.load(f)

    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=12418",
        json=outcome,
    )
    return requests_mock


@pytest.fixture
def rum_runner_mock(requests_mock):
    with open("resources/rum_runner.json") as f:
        outcome = json.load(f)

    requests_mock.get(
        "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i=16250",
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
    assert cocktails["11021"] == "Allegheny"
    assert cocktails["12418"] == "Turf Cocktail"
    assert cocktails["13775"] == "Jelly Bean"
    assert cocktails["16250"] == "Rum Runner"


def test_get_cocktail2ingredients(
    allegheny_mock, jelly_bean_mock, rum_runner_mock, turf_cocktail_mock
):
    cocktail_ids = {
        "11021": "Allegheny",
        "12418": "Turf Cocktail",
        "13775": "Jelly Bean",
        "16250": "Rum Runner",
    }

    cocktail2ingredients = get_cocktail2ingredients(cocktail_ids)

    assert len(cocktail2ingredients) == 4

    assert cocktail2ingredients["11021"]["ingredients"] == [
        "Blackberry brandy",
        "Bourbon",
        "Dry Vermouth",
        "Lemon juice",
        "Lemon peel",
    ]

    assert cocktail2ingredients["12418"]["ingredients"] == [
        "Anis",
        "Bitters",
        "Dry Vermouth",
        "Gin",
        "Orange peel",
    ]
    assert cocktail2ingredients["13775"]["ingredients"] == [
        "Anis",
        "Blackberry brandy",
    ]
    assert cocktail2ingredients["16250"]["ingredients"] == [
        "Blackberry brandy",
        "Cranberry juice",
        "Malibu rum",
        "Orange juice",
        "Pineapple juice",
    ]


def test_what_cocktail_can_i_make():
    cocktail2ingredients = {
        "11021": {
            "name": "Allegheny",
            "ingredients": [
                "Blackberry brandy",
                "Bourbon",
                "Dry Vermouth",
                "Lemon juice",
                "Lemon peel",
            ],
        },
        "12418": {
            "name": "Turf Cocktail",
            "ingredients": [
                "Anis",
                "Bitters",
                "Dry Vermouth",
                "Gin",
                "Orange peel",
            ],
        },
        "13775": {
            "name": "Jelly Bean",
            "ingredients": ["Anis", "Blackberry brandy"],
        },
        "16250": {
            "name": "Rum Runner",
            "ingredients": [
                "Blackberry brandy",
                "Cranberry juice",
                "Malibu rum",
                "Orange juice",
                "Pineapple juice",
            ],
        },
    }
    ingredients = ["Anis", "Blackberry brandy"]

    cocktails = what_cocktail_can_i_make(cocktail2ingredients, ingredients)


def test_get_cocktails():
    ingredients = ["Anis", "Blackberry brandy"]
    cocktails = get_cocktails(ingredients)
    assert len(cocktails) == 1
    assert cocktails[0]["name"] == "Jelly Bean"
    assert cocktails[0]["id"] == "13775"
