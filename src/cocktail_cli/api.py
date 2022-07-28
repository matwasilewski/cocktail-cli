import logging
from datetime import timedelta
from typing import List

import requests
from requests_cache import CachedSession

session = CachedSession(
    "cocktails_cache",
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
cocktail_url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php"


def cocktails_with_ingredients(ingredients: List[str]):
    headers = {"Accept": "application/json"}
    payload = {"i": ingredients}
    resp = session.get(cocktail_url, params=payload, headers=headers)
    try:
        cocktails = resp.json()["drinks"]
    except:
        cocktails = []
        logging.warning(f"At least one component of {ingredients} is unknown!")

    return cocktails
