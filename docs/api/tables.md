# ORM Tables

{mod}`unihan_db.tables` defines the
[SQLAlchemy](https://www.sqlalchemy.org/) ORM schema for [UNIHAN] data.
{attr}`unihan_db.tables.Base.metadata` owns the shared metadata, and
{class}`unihan_db.tables.Unhn` is the central character table that readings,
dictionary locations, IRG source records, radical/stroke data, and indexes
relate back to.

[UNIHAN]: https://www.unicode.org/charts/unihan.html

```{eval-rst}
.. automodule:: unihan_db.tables
   :members:
   :undoc-members:
   :show-inheritance:
```
