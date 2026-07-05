(api)=

# API Reference

:::{warning}
Be careful with these! APIs are **not** considered stable before 1.0 and may
change or be removed between minor versions.

If you need an internal API stabilized please [file an issue](https://github.com/cihai/unihan-db/issues).
:::

Most projects only need the bootstrap path: create a
[SQLAlchemy](https://www.sqlalchemy.org/) session, run
{func}`unihan_db.bootstrap.bootstrap_unihan`, and query
{class}`unihan_db.tables.Unhn`. The reference pages below split the API by the
same pipeline: load data, turn records into rows, then query the mapped tables.

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Bootstrap
:link: bootstrap
:link-type: doc
Data download, session helpers, and ETL options.
:::

:::{grid-item-card} Importer
:link: importer
:link-type: doc
Transform normalized UNIHAN records into ORM objects.
:::

:::{grid-item-card} Tables
:link: tables
:link-type: doc
SQLAlchemy ORM models for UNIHAN data.
:::

::::

```{toctree}
:caption: API
:maxdepth: 1
:hidden:

bootstrap
importer
tables
```
