import csv
from pathlib import Path

DATABASE_PATH = Path("products.tsv")


if not DATABASE_PATH.exists():
    DATABASE_PATH.touch()

TsvRow = list[str]


def load_products() -> list[dict]:
    """Load all products from the database file."""
    with DATABASE_PATH.open("r") as file:
        reader = csv.reader(file, delimiter="\t")
        return list(map(_deserialize_product, reader))


def save_products(products: list[dict]) -> None:
    """Save all products to the database file."""
    with DATABASE_PATH.open("w") as file:
        reader = csv.writer(file, delimiter="\t")
        reader.writerows(map(_serialize_product, products))


def _deserialize_product(row: TsvRow) -> dict:
    return dict(id=int(row[0]), name=row[1], description=row[2], price=int(row[3]))


def _serialize_product(product: dict) -> TsvRow:
    return [product["id"], product["name"], product["description"], product["price"]]
