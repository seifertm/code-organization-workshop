import spacy
from fastapi import FastAPI, HTTPException
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
import json


app = FastAPI()

DATABASE_PATH = Path("products.json")


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: int
    """Price in Euro cents"""


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


@app.get("/products")
def get_all_products() -> list[Product]:
    products = load_products()
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int) -> Product:
    products = load_products()

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products")
def create_product(product: Product) -> Product:
    products = load_products()

    product.id = max([p["id"] for p in products], default=0) + 1
    products.append(product.model_dump())

    save_products(products)

    return product


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product) -> Product:
    products = load_products()

    for i, p in enumerate(products):
        if p["id"] == product_id:
            products[i] = product.model_dump()

            save_products(products)

            return product

    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products/{product_id}")
def delete_product(product_id: int) -> Product:
    products = load_products()

    for index, product in enumerate(products):
        if product["id"] == product_id:
            deleted_product = products.pop(index)

            save_products(products)

            return deleted_product

    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/description-similarity")
def product_description_similarity(product_id0: int, product_id1: int) -> dict:
    products = load_products()
    product0 = product1 = None
    for product in products:
        if product["id"] == product_id0:
            product0 = product
        elif product["id"] == product_id1:
            product1 = product
    if not product0:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id0} not found"
        )
    if not product1:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id1} not found"
        )

    nlp = spacy.load("en_core_web_md")
    description0 = nlp(product0["description"])
    description1 = nlp(product1["description"])
    return {"similarity": description0.similarity(description1)}


@app.get("/name-similarity")
def product_name_similarity(product_id0: int, product_id1: int) -> dict:
    products = load_products()
    product0 = product1 = None
    for product in products:
        if product["id"] == product_id0:
            product0 = product
        elif product["id"] == product_id1:
            product1 = product
    if not product0:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id0} not found"
        )
    if not product1:
        raise HTTPException(
            status_code=404, detail=f"Product with ID {product_id1} not found"
        )

    nlp = spacy.load("en_core_web_md")
    name0 = nlp(product0["name"])
    name1 = nlp(product1["name"])
    return {"similarity": name0.similarity(name1)}
