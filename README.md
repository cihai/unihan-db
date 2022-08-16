# unihan-db &middot; [![Python Package](https://img.shields.io/pypi/v/unihan-db.svg)](https://pypi.org/project/unihan-db/) [![License](https://img.shields.io/github/license/cihai/unihan-db.svg)](https://github.com/cihai/unihan-db/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/cihai/unihan-db/branch/master/graph/badge.svg)](https://codecov.io/gh/cihai/unihan-db)

Database [SQLAlchemy](https://www.sqlalchemy.org/) models for
[UNIHAN](http://www.unicode.org/charts/unihan.html). Part of the [cihai](https://cihai.git-pull.com)
project. Powered by [unihan-etl](https://unihan-etl.git-pull.com). See also:
[libUnihan](http://libunihan.sourceforge.net/).

By default, unihan-db creates a SQLite database in an
[XDG data directory](https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html). You
can specify a custom database destination by passing a database url into
[get_session](http://unihan-db.git-pull.com/api.html#unihan_db.bootstrap.get_session).

## Example usage

```python
#!/usr/bin/env python
import pprint

from sqlalchemy.sql.expression import func

from unihan_db import bootstrap
from unihan_db.tables import Unhn

session = bootstrap.get_session()

bootstrap.bootstrap_unihan(session)

random_row = session.query(Unhn).order_by(
    func.random()
).limit(1).first()

pp = pprint.PrettyPrinter(indent=0)

pp.pprint(random_row.to_dict())
```

Run:

    $ ./examples/01_bootstrap.py

Output:

```python
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
$ git clone https://github.com/cihai/unihan-etl.git
```

```console
$ cd unihan-etl
```

[Bootstrap your environment and learn more about contributing](https://cihai.git-pull.com/contributing/). We use the same conventions / tools across all cihai projects: `pytest`, `sphinx`, `flake8`, `mypy`, `black`, `isort`, `tmuxp`, and file watcher helpers (e.g. `entr(1)`).

## More information

[![Docs](https://github.com/cihai/unihan-db/workflows/docs/badge.svg)](https://unihan-db.git-pull.com/)
[![Build Status](https://github.com/cihai/unihan-db/workflows/tests/badge.svg)](https://github.com/cihai/unihan-db/actions?query=workflow%3A%22tests%22)
