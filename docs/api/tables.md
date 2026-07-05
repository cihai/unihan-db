# ORM Tables

{mod}`unihan_db.tables` defines the
[SQLAlchemy](https://www.sqlalchemy.org/) ORM schema for UNIHAN data.
{class}`unihan_db.tables.Base` owns the shared metadata, and
{class}`unihan_db.tables.Unhn` is the central character table that readings,
dictionary locations, variant forms, and indexes relate back to.

```{eval-rst}
.. automodule:: unihan_db.tables
   :members:
   :undoc-members:
   :show-inheritance:
```
