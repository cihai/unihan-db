# Importer Internals

{mod}`unihan_db.importer` turns normalized
[unihan-etl](https://unihan-etl.git-pull.com/) records into ORM rows. Most users
do not call it directly; {func}`unihan_db.bootstrap.bootstrap_unihan` calls
{func}`unihan_db.importer.import_char` while loading
{class}`unihan_db.tables.Unhn` and its related tables.

```{eval-rst}
.. automodule:: unihan_db.importer
   :members:
   :undoc-members:
   :show-inheritance:
```
