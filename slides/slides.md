## Code Organization for non-engineers

2026-07-13 – Michael Seifert

Notes:
- Out of scope:
  - Linting and static analysis
  - DRY, KISS, YAGNI, SOLID, GoF patterns

---

## Application Layers

![](application-layers.svg)

---


## Cohesion

A component's degree of focus.

---

## Outline

1. Structuring Code within a Module
1. Structuring Code across Modules <!-- .element: class="fragment" -->
1. Training Wheels are Off <!-- .element: class="fragment" -->
1. Dependency Injection <!-- .element: class="fragment" -->
1. Recap <!-- .element: class="fragment" -->

---

## Part 1: Structuring Code within a Module

--

## Hands On
`git clone https://github.com/seifertm/code-organization-workshop.git`

--

## Take a Break

--

## Recap

- We identified that it's hard to make the code change we want to do
- We wrote tests to avoid accidental breakage of our application <!-- .element: class="fragment" -->
- We refactored the code to make the database switch simpler <!-- .element: class="fragment" -->

Notes:
- In a way, automated tests and refactoring are was to derisk your project

--

## Take Aways

- Duplication makes code harder to change
- Automated tests give confidence when refactoring <!-- .element: class="fragment" -->
- Centralizing database operations made the code more testable <!-- .element: class="fragment" -->

--

## Tips

- There are often several levels of tests
- Don't refactor test code as hard as production code <!-- .element: class="fragment" -->
- The "Rule of Three" (Fowler et al. (1999))  is a good guideline for preventing code duplication <!-- .element: class="fragment" -->

Notes:

- Analogy between different levels of tests and a broken car


---

## Part 2: Structuring Code across Modules

--

## Hands On

--

## Take a Break

--

## Recap

- We introduced a new application layer

![](db-layer.svg)

Notes:
- An application layer can have multiple modules or packages
- Each application layer usually has its own data model

--

## Take Aways

- Module imports can help identify modules with low cohesion
- Modules with high cohesion are easy to substitute <!-- .element: class="fragment" -->

--

## Tips

- Implement connections to external systems in separate modules
- Keep API surfaces as small as possible <!-- .element: class="fragment" -->

Notes:
- *API* in this case refers to general programming interfaces, not just to web APIs.
- Both points can be found in prolific software engineering literatur, such as Clean Architecture, Hexagonal Architecture, or DDD

---

## Part 3: Training Wheels are Off

--

## Hands On

--

## Discussion

---

## Part 4: Dependency Injection

--

``` python
def migrate_data():
    json_db_settings = load_database_config(…)
    json_db = init_database(…)

    tsv_db_settings = load_database_config(…)
    tsv_db = init_database(…)

    products = json_db.load_products(…)
    tsv_db.save_products(products)

    json_db.close()
    tsv_db.close()
```

Notes:
- How can you test this function?
- How cohesive is this function?

--

``` python
def migrate_data(json_db, tsv_db):
    products = json_db.load_products(…)
    tsv_db.save_products(products)
```

``` python
def main():
    json_db_settings = load_database_config(…)
    json_db = init_database(…)

    tsv_db_settings = load_database_config(…)
    tsv_db = init_database(…)

    migrate_data(json_db, tsv_db)

    json_db.close()
    tsv_db.close()
```

Notes:
- Migrate data is easier to test in isolation
- Database setup code was hoisted up. It is reusable at a higher level

--

## Hands On

--

## Take aways

- Dependency injection moves cohesion in our call stack
- Keep cohesion high

---

## Recap

1. Structuring Code within a Module
1. Structuring Code across Modules <!-- .element: class="fragment" -->
1. Training Wheels are Off <!-- .element: class="fragment" -->
1. Dependency Injection <!-- .element: class="fragment" -->

---

## Summary

- Testing and refactoring are not an end in itself. Both serve a purpose.
- Be conscious about whether you're currently taking a shortcut or not <!-- .element: class="fragment" -->
- Make mistakes and learn from them (=> go back to your old code) <!-- .element: class="fragment" -->

---

## Feedback

<figure class="r-stretch">
    <img src="feedback.svg" width="600px" height="auto" style="object-fit: contain;" />
</figure>

---

## References

[Stevens at al. (1974). Structured design. IBM Systems Journal.](doi:10.1147/sj.132.0115)

Fowler et. al (1999). Refactoring: Improving the Design of Existing Code. Addison-Wesley Professional. ISBN 978-0201485677
