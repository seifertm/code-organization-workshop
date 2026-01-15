import json
from pathlib import Path

DATABASE_PATH = Path("products.json")


if not DATABASE_PATH.exists():
    with DATABASE_PATH.open("w") as file:
        json.dump([], file)


def load_products() -> list[dict]:
    """Load all products from the database file."""
    with DATABASE_PATH.open("r") as file:
        return json.load(file)


def save_products(products: list[dict]) -> None:
    """Save all products to the database file."""
    with DATABASE_PATH.open("w") as file:
        json.dump(products, file, indent=2)
