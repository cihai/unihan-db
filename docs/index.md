(index)=

# unihan-db

[SQLAlchemy](https://www.sqlalchemy.org/) models for the [UNIHAN](https://www.unicode.org/charts/unihan.html) CJK character database.
unihan-db provides the schema and ORM layer. For the ETL pipeline, see [unihan-etl](https://unihan-etl.git-pull.com/). For end-user character lookups, see [cihai](https://cihai.git-pull.com/).

Most projects use {func}`unihan_db.bootstrap.get_session` or their own SQLAlchemy
engine, load the data once with {func}`unihan_db.bootstrap.bootstrap_unihan`, and
then query {class}`unihan_db.tables.Unhn` and the tables that hang off it.

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Quickstart
:link: quickstart
:link-type: doc
Install and load UNIHAN data in 5 minutes.
:::

:::{grid-item-card} How-to Guides
:link: how-to/index
:link-type: doc
Common tasks: custom databases, offline bootstraps, and ORM queries.
:::

:::{grid-item-card} Models & Bootstrap
:link: api/index
:link-type: doc
Table models, bootstrap helpers, and importer internals.
:::

:::{grid-item-card} Explanation
:link: explanation/index
:link-type: doc
How the ETL pipeline, bootstrap step, and ORM schema fit together.
:::

:::{grid-item-card} Contributing
:link: project/index
:link-type: doc
Development setup, code style, release process.
:::

::::

## Install

```console
$ pip install unihan-db
```

```console
$ uv add unihan-db
```

## At a glance

The same bootstrap example appears in the quickstart and is executed by the test
suite.

```{literalinclude} ../examples/01_bootstrap.py
:language: python
```

See {doc}`quickstart` for the full setup, including bootstrapping
data from the Unicode consortium.

```{toctree}
:hidden:

quickstart
how-to/index
api/index
explanation/index
project/index
history
GitHub <https://github.com/cihai/unihan-db>
```
