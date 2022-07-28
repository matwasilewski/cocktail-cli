from typing import List

import requests

cocktail_url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php"


def cocktails_from_ingredients(ingredients: List[str]):
    payload = {"i": ingredients}
    resp = requests.get(cocktail_url, params=payload)
    return resp
