# unihan-db &middot; [![Python Package](https://img.shields.io/pypi/v/unihan-db.svg)](https://pypi.org/project/unihan-db/) [![License](https://img.shields.io/github/license/cihai/unihan-db.svg)](https://github.com/cihai/unihan-db/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/cihai/unihan-db/branch/master/graph/badge.svg)](https://codecov.io/gh/cihai/unihan-db)

Database [SQLAlchemy](https://www.sqlalchemy.org/) models for
[UNIHAN](http://www.unicode.org/charts/unihan.html). Part of the [cihai](https://cihai.git-pull.com)
project. Powered by [unihan-etl](https://unihan-etl.git-pull.com). See also:
[libUnihan](http://libunihan.sourceforge.net/).

By default, unihan-db creates a SQLite database in an
[XDG data directory](https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html). You
can specify a custom database destination by passing a database url into
[get_session](https://unihan-db.git-pull.com/api/bootstrap.html#unihan_db.bootstrap.get_session).

## Install

Use [Python](https://www.python.org/) 3.10 or newer, below 4.0.

```console
$ pip install unihan-db
```

```console
$ uv add unihan-db
```

## Example usage

This is `examples/01_bootstrap.py`, included in the source tree — running it
as shown needs a clone (see [Developing](#developing)).

```python
#!/usr/bin/env python
"""Example for bootstrapping UNIHAN DB."""

from __future__ import annotations

import logging
import pprint

from sqlalchemy.sql.expression import func

from unihan_db import bootstrap
from unihan_db.tables import Unhn

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


def run(unihan_options: dict[str, object] | None = None) -> None:
    """Initialize Unihan DB via ``bootstrap_unihan()``."""
    session = bootstrap.get_session()

    bootstrap.bootstrap_unihan(session, unihan_options)

    random_row_query = session.query(Unhn).order_by(func.random()).limit(1)

    assert random_row_query is not None

    random_row = random_row_query.first()

    log.info(pprint.pformat(bootstrap.to_dict(random_row)))

    assert random_row is not None

    log.info(pprint.pformat(random_row.to_dict()))  # type:ignore


if __name__ == "__main__":
    run()
```

Run:

    $ ./examples/01_bootstrap.py

Output (one random character; yours will differ):

```text
{'char': '鎷',
'kCantonese': [{'char_id': '鎷', 'definition': 'maa5', 'id': 24035}],
'kDefinition': [],
'kHanYu': [{'char_id': '鎷',
          'id': 24014,
          'locations': [{'character': 5,
                       'generic_indice_id': 24014,
                       'generic_reading_id': None,
                       'id': 42170,
                       'page': 4237,
                       'virtual': 0,
                       'volume': 6}],
          'type': 'kHanYu'}],
'kHanyuPinyin': [{'char_id': '鎷',
                'id': 18090,
                'locations': [{'character': 5,
                             'generic_indice_id': None,
                             'generic_reading_id': 18090,
                             'id': 42169,
                             'page': 4237,
                             'virtual': 0,
                             'volume': 6}],
                'readings': [{'generic_reading_id': 18090,
                            'id': 26695,
                            'reading': 'mǎ'}],
                'type': 'kHanyuPinyin'}],
'kMandarin': [{'char_id': '鎷', 'hans': 'mǎ', 'hant': 'mǎ', 'id': 23486}],
'ucn': 'U+93B7'}
```

## Developing

```console
$ git clone https://github.com/cihai/unihan-db.git
```

```console
$ cd unihan-db
```

See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md) for the gates and
commands. unihan-db follows the
[cihai contributing guide](https://cihai.git-pull.com/project/contributing/)
for conventions shared across the cihai family: `pytest`, `sphinx`, `mypy`,
`ruff`, `tmuxp`, and file watcher helpers such as `entr(1)`.

## Python versions

Requires Python 3.10 or newer, below 4.0 (see [Install](#install)). Older
releases supported earlier interpreters:

- 0.8.0:
  - Last Python 3.7 release
  - Last SQLAlchemy 1.3 release

## More information

[![Docs](https://github.com/cihai/unihan-db/workflows/docs/badge.svg)](https://unihan-db.git-pull.com/)
[![Build Status](https://github.com/cihai/unihan-db/workflows/tests/badge.svg)](https://github.com/cihai/unihan-db/actions?query=workflow%3A%22tests%22)
