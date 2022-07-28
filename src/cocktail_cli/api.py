import logging
from typing import List

import requests

cocktail_url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php"


def cocktails_with_ingredients(ingredients: List[str]):
    headers = {'Accept': 'application/json'}
    payload = {"i": ingredients}
    resp = requests.get(cocktail_url, params=payload, headers=headers)

    try:
        cocktails = resp.json()["drinks"]
    except:
        cocktails = []
        logging.warning(f"At least one component of {ingredients} is unknown!")

    return cocktails
