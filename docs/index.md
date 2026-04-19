(index)=

# unihan-db

SQLAlchemy models for the [UNIHAN](https://www.unicode.org/charts/unihan.html) CJK character database.
unihan-db provides the schema and ORM layer. For the ETL pipeline, see [unihan-etl](https://unihan-etl.git-pull.com/). For end-user character lookups, see [cihai](https://cihai.git-pull.com/).

::::{grid} 1 2 3 3
:gutter: 2 2 3 3

:::{grid-item-card} Quickstart
:link: quickstart
:link-type: doc
Install and load UNIHAN data in 5 minutes.
:::

:::{grid-item-card} Models & Bootstrap
:link: api/index
:link-type: doc
Table models, bootstrap loader, and data importer.
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

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from unihan_db.bootstrap import bootstrap_unihan
from unihan_db.tables import Base, Unhn

engine = create_engine("sqlite:///unihan.db")

# Step 1: Create the schema
Base.metadata.create_all(engine)

# Step 2: Bootstrap data from the Unicode consortium
bootstrap_unihan(engine)

# Step 3: Query characters
with Session(engine) as session:
    char = session.query(Unhn).filter_by(char="\u597D").first()
    if char:
        print(char.char, char.ucn)
```

See [Quickstart](quickstart.md) for the full setup, including bootstrapping
data from the Unicode consortium.

```{toctree}
:hidden:

quickstart
api/index
project/index
history
GitHub <https://github.com/cihai/unihan-db>
```
