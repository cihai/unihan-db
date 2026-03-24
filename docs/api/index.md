(api)=

# API Reference

```{module} unihan_db

```

:::{warning}
Be careful with these! APIs are **not** covered considered stable pre-1.0. They can break or be removed between minor versions!

If you need an internal API stabilized please [file an issue](https://github.com/cihai/unihan-db/issues).
:::

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
