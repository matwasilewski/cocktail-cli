import logging
from datetime import timedelta
from json import JSONDecodeError
from typing import List, Dict

import requests
from requests_cache import CachedSession

from src.cocktail_cli.exceptions import (
    CocktailDetailsException,
    CocktailAPIException,
)

session = CachedSession(
    "mycache",
    use_cache_dir=True,
    cache_control=True,
    expire_after=timedelta(days=1),
    allowable_methods=[
        "GET",
        "POST",
    ],
    allowable_codes=[
        200,
        400,
    ],
    ignored_parameters=["api_key"],
    match_headers=True,
    stale_if_error=True,
)

filter_url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php"


def cocktails_with_ingredient(ingredient: str) -> List[str]:
    headers = {"Accept": "application/json"}
    payload = {"i": ingredient}

    try:
        resp = session.get(filter_url, params=payload, headers=headers)
        assert resp.status_code == 200
        cocktails = resp.json()["drinks"]
    except AssertionError:
        logging.error(f"Non-200 exception code: {resp.status_code}")
        raise CocktailAPIException("Non-200 exception in {resp}")
    except (JSONDecodeError, KeyError):
        cocktails = []
        logging.warning(f"At least one component of {ingredient} is unknown!")
    return cocktails


def cocktail_components_from_id(cocktail_id: str) -> List[str]:
    url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cocktail_id}"
    return cocktail_components(url)


def cocktail_components(cocktail_url) -> List[str]:
    headers = {"Accept": "application/json"}
    ingredients = set()

    try:
        resp = session.get(
            cocktail_url,
            headers=headers,
        )
        assert resp.status_code == 200

        details = resp.json()["drinks"][0]

        for i in range(1, 16):
            if details.get(f"strIngredient{i}", None):
                ingredients.add(details.get(f"strIngredient{i}", None))
    except AssertionError:
        logging.error(f"Non-200 exception code: {resp.status_code}")
        raise CocktailAPIException("Non-200 exception in {resp}")
    except KeyError:
        logging.error(f"Unexpected response outcome!")
        raise CocktailDetailsException()

    return sorted(list(ingredients))


def get_cocktails_that_have_given_ingredients(components: List[str]):
    cocktail_ids = {}

    for component in components:
        cocktails_from_component = cocktails_with_ingredient(component)
        for cocktail in cocktails_from_component:
            cocktail_ids[cocktail["idDrink"]] = cocktail["strDrink"]

    return cocktail_ids


def get_cocktail2ingredients(
    cocktail_ids: Dict[str, str],
) -> dict[str, dict[str, str | list[str]]]:
    cocktail2ingredients = {}

    for cocktail_id, cocktail_name in cocktail_ids.items():
        cocktail2ingredients[cocktail_id] = {
            "name": cocktail_name,
            "ingredients": cocktail_components_from_id(cocktail_id),
        }

    return cocktail2ingredients


def what_cocktail_can_i_make(cocktail2ingredients: Dict, ingredients: List):

    can_make = []
    ingredients = set([ing.lower() for ing in set(ingredients)])

    for cocktail_id, cocktail_ingredients in cocktail2ingredients.items():
        this_cocktail_ingredients = {
            ing.lower() for ing in cocktail_ingredients["ingredients"]
        }
        if len(this_cocktail_ingredients.difference(ingredients)) == 0:
            can_make.append(
                {
                    "name": cocktail_ingredients["name"],
                    "id": cocktail_id,
                }
            )

    return can_make


def get_cocktails(ingredients):
    cocktails_that_contain_some_ingredients = (
        get_cocktails_that_have_given_ingredients(ingredients)
    )

    concktail2ingredient = get_cocktail2ingredients(
        cocktails_that_contain_some_ingredients
    )

    cocktails = what_cocktail_can_i_make(concktail2ingredient, ingredients)
    return cocktails
