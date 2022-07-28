# Cocktail CLI

This is command-line app that returns what cocktails can be made using given components.

## Installation

To install the app, install the wheel:
```python
pip install dist/cocktail_cli-0.1.2-py3-none-any.whl
```

Voila!

## How-to

The app accepts a path to a file with comma-separated ingredients that user has in their pantry.

Sample file with ingredients:

```
Anis,Blackberry brandy,vodka
```

Sample command (using `pantry.csv` from test resources):
```bash
cocktail tests/pantry.csv
```