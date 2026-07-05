# Bootstrap Helpers

{mod}`unihan_db.bootstrap` is the load layer: it asks
[unihan-etl](https://unihan-etl.git-pull.com/) for normalized UNIHAN records,
creates the schema, and inserts rows when the database is still empty. For most
uses, call {func}`unihan_db.bootstrap.get_session` for the default SQLite-backed
session, then call {func}`unihan_db.bootstrap.bootstrap_unihan` once before
querying.

For the rarer cases, {func}`unihan_db.bootstrap.bootstrap_data` exposes the ETL
options, and {func}`unihan_db.bootstrap.to_dict` turns ORM rows into plain
dictionaries for display or serialization.

```{eval-rst}
.. automodule:: unihan_db.bootstrap
   :members:
   :undoc-members:
   :show-inheritance:
```
