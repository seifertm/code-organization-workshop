This repository contains exercises for a workshop on code organization.

# Prerequisites

- [uv](https://docs.astral.sh/uv/)


# Part 1: Structuring Code Within a Module

## Exercise 0

- Install a SpaCy model file: `uv pip install en_core_web_md@https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl`
- Run the web application with the command `uv run fastapi dev src/tutorial_app/app.py`
- Open the URL to the API documentation that is printed on the terminal. The page shows the OpenAPI documentation of the API.
- Use the OpenAPI documentation page to issue example requests. Create at least three different products using the *POST /product* endpoint. Try out one of the endpoints that compute a similarity score between two product descriptions or names.
- Verify that the file *products.json* is created in your project directory.

Imagine that *products.json* is a full fledged, managed database by a commercial vendor. We will refer to *products.json* as "The JSON database" from now on.


## Exercise 1 (Group exercise)
*JSON Cloud Services*, the company behind The JSON Database (i.e. *products.json*), changes its pricing model which leads to a tenfold cost increase for your application. Due to the steep price increase, your company decides to deprecate all use of The JSON Database. You can no longer use *products.json* as your database and you are forced to migrate away from it by the end of this workshop (no pressure ;).

Everyone agrees that the most future-proof storage solution is *products.tsv* (Tab Separated Values). Somebody already created a script that will migrate all data from The JSON Database to new database. All that remains is adjusting your application to use the new database.

Which lines of code do you have to change to switch out The JSON Database with *products.tsv*?


## Exercise 2

We're going to replace The JSON Database in the web application. Before we change the code, we will write an automated test. This will help us catch errors that are accidentally introduced during refactoring. Do *not* change any code in `src/tutorial_app/app.py`.

Navigate to `tests/test_app.py` and follow the instructions in the file


## Exercise 3

The logic for loading products from the database and storing them in the database is duplicated multiple times throughout the code. This makes it hard to change any database-related code. Create two new functions, `load_products() -> list[dict]`, which retrieves all products from the database, and `save_products(products: list[dict] -> None` which stores a list of products in the database. Refactor `src/tutorial_app/app.py` so that all operations for loading and storing products use those two functions.

Do *not* change the behavior of the code, only its structure. This means that no modification of the tests is necessary.

Run the tests frequently to make sure all tests run successfully at every step of your refactoring.


## Bonus exercise 1
By centralizing the logic for database operations in the respective load and save functions, we made it possible to test database-related functionality in isolation from the rest of the application.

Write automated tests for the database functionality

Make sure all tests run successfully.


## Bonus exercise 2
The functions `load_products` and `save_products` both operate on `list[dict]`. Here, a dictionary represents product data. A developer who is unfamiliar with the application will not understand the contents of `dict` solely based on the type siganture. They will have to figure out the structure of those dictionaries by looking at the code that uses the respective functions.

Think of ways to make it easier for the reader to understand which attributes represent a Product.


# Part 2: Structuring Code Across Modules

## Exercise 4 (group exercise)

Explain the purpose of the `src/tutorial_app/app.py` module in one sentence.


## Exercise 5

The module `src/tutorial_app/app.py` has many different responsibilities. We're still not done replacing The JSON Database.

Move all database-related functionality to the new Python module `src/tutorial_app/json_db.py`. This includes the code that creates an empty database if *products.json* doesn't exist.

Make sure all tests run successfully.

Explain the purpose of `src/tutorial_app/json_db.py` in the module docstring.

Look at the file `src/tutorial_app/app.py`. Notice how all imports related to The JSON Database, namely `json` and `pathlib` have disappeared from *app.py*.

Module imports are usually a good indication how many different responsibilities a module has. If a module uses imports from many different layers of your application, it likely has many responsibilities. Multiple responsibilities introduce complexity, which makes the module harder to understand. A module with few unrelated imports is very focused. This is called high *cohesion* in software engineering terms and is very desirable. We prefer modules with high cohesion.


## Exercise 6

Create a new module `src/tutorial_app/tsv_db.py`.
Use the [csv module](https://docs.python.org/3/library/csv.html) from the Python standard library to implement the functions `save_products` and `load_products` in the new module. Keep the function signatures the same as in `json_db.py`.

You can use the following helper functions to convert a product dictionary to a row in the TSV file and vice versa:

``` python
TsvRow = list[str]


def _serialize_product(product: dict) -> TsvRow:
    return [product["id"], product["name"], product["description"], product["price"]]


def _deserialize_product(row: TsvRow) -> dict:
    return dict(id=int(row[0]), name=row[1], description=row[2], price=int(row[3]))
```

Which lines of code do you need to change to switch to the new database? How does it compare to the initial version?

Change *app.py* so it actually uses *tsv_db*, instead of *json_db*.


## Bonus Exercise 1

Notice that we have two different database implementations in *json_db* and *tsv_db*, both of which have the same API.
To hide the actual database implementation from its callers, software engineers often resort to a structure called the *Repository pattern*. Read up about the [Repository pattern](https://web.archive.org/web/20260111223620/https://www.cosmicpython.com/book/chapter_02_repository.html) and think how you can apply this pattern in our current application.


# Part 3: Training Wheels are Off

## Exercise 7

The existing approach to computing the similarity score between two product names or descriptions uses word embeddings and cosine similarity. You found out that a similarity score using the Levenshtein distance is less computationally expensive, while yielding good enough results. The business wants you to switch to the Levenshtein scoring.
 
Perform the following steps without making breaking changes to the API endpoints:
- Deduplicate the existing code that uses SpaCy to compute the similarity score.  
- Move all code related to the similarity scoring into a separate module.
- Implement a similarity scoring for two strings based on the Levenshtein distance

Note: You can use [Levenshtein.ratio](https://rapidfuzz.github.io/Levenshtein/levenshtein.html#Levenshtein.ratio) for calculating the actual scoring.


## Bonus Exercise 1
FastAPI allows grouping API endpoints via the [ApiRouter](https://fastapi.tiangolo.com/tutorial/bigger-applications/) class. Separate the endpoints for similarity scoring from the endpoints that provide operations on products into different modules. 

