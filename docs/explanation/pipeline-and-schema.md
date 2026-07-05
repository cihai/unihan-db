(pipeline-and-schema)=

# Pipeline and Schema

unihan-db has one main path: [unihan-etl](https://unihan-etl.git-pull.com/)
fetches and normalizes [UNIHAN](https://www.unicode.org/charts/unihan.html)
records, {func}`unihan_db.bootstrap.bootstrap_unihan` inserts those records
once, and application code queries {class}`unihan_db.tables.Unhn` through
[SQLAlchemy](https://www.sqlalchemy.org/).

{func}`unihan_db.bootstrap.get_session` is the default entry point for
applications. It creates the schema and returns a scoped SQLAlchemy session
bound to the default SQLite database. Use a custom database URL only when your
application needs to control where the database lives.

{mod}`unihan_db.importer` is the narrower layer that turns normalized records
into ORM objects. Most users do not call it directly; it exists so the bootstrap
step can keep download/export concerns separate from row construction.

{mod}`unihan_db.tables` is the reference surface for the mapped tables. The
central model is {class}`unihan_db.tables.Unhn`; related reading, dictionary
location, radical/stroke, source, and index rows connect back to that character
row.
