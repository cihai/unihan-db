(custom-database)=

# Use a Custom Database

{func}`unihan_db.bootstrap.get_session` stores the default SQLite database in
the current user's XDG data directory. Pass an explicit SQLAlchemy database URL
when your application should own the database location.

Use a file URL such as `sqlite:////path/to/unihan.db` for a persistent SQLite
database. After you have the session, the rest of the workflow is unchanged:
call {func}`unihan_db.bootstrap.bootstrap_unihan` once, then query
{class}`unihan_db.tables.Unhn` rows.

```{doctest}
>>> from unihan_db.bootstrap import get_session
>>> db_path = tmp_path / "unihan.db"
>>> session = get_session(f"sqlite:///{db_path}")
>>> db_path.exists()
True
>>> session.remove()
```

For test suites, prefer an in-memory SQLAlchemy engine and the fixtures in
`tests/` so the first bootstrap can use a local UNIHAN archive instead of the
network.
