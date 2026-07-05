(query-related-tables)=

# Query Local Rows

Once the schema exists, querying unihan-db is ordinary
[SQLAlchemy](https://www.sqlalchemy.org/) ORM work. The central table is
{class}`unihan_db.tables.Unhn`; related reading, dictionary-location,
radical/stroke, source, and index tables hang off each character row.

The small example below stays offline by creating one row directly instead of
running the full UNIHAN bootstrap.

```{doctest}
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import Session
>>> from unihan_db.bootstrap import to_dict
>>> from unihan_db.tables import Base, Unhn
>>> engine = create_engine("sqlite:///:memory:")
>>> Base.metadata.create_all(engine)
>>> session = Session(engine)
>>> session.add(Unhn(char="好", ucn="U+597D"))
>>> session.commit()
>>> row = session.query(Unhn).filter_by(char="好").one()
>>> row.char, row.ucn
('好', 'U+597D')
>>> to_dict(row)["char"]
'好'
>>> session.close()
```

Use {func}`unihan_db.bootstrap.to_dict` when you need a plain dictionary for
display or serialization. For real data, call
{func}`unihan_db.bootstrap.bootstrap_unihan` before running the query.
