*unihan-db* - database `SQLAlchemy`_ models for `UNIHAN`_. Part of the `cihai`_
project. Powered by `unihan-etl`_. See also: `libUnihan`_.

|pypi| |docs| |build-status| |coverage| |license|

By default, unihan-db creates a SQLite database in an `XDG data directory`_.
You can specify a custom database destination by passing a database url
into `get_session`_.

.. _SQLAlchemy: https://www.sqlalchemy.org/
.. _get_session: http://unihan-db.git-pull.com/en/latest/api.html#unihan_db.bootstrap.get_session
.. _XDG data directory: https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html

Example usage
-------------
.. code-block:: python

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

Run::

   $ ./examples/01_bootstrap.py

Output:

.. code-block:: python

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

Developing
----------
`poetry`_ is a required package to develop.

``git clone https://github.com/cihai/unihan-etl.git``

``cd unihan-etl``

``poetry install -E "docs test coverage lint format"``

Makefile commands prefixed with ``watch_`` will watch files and rerun.

Tests
"""""

``poetry run py.test``

Helpers: ``make test``
Rerun tests on file change: ``make watch_test`` (requires `entr(1)`_)

Documentation
"""""""""""""
Default preview server: http://localhost:8041

``cd docs/`` and ``make html`` to build. ``make serve`` to start http server.

Helpers:
``make build_docs``, ``make serve_docs``

Rebuild docs on file change: ``make watch_docs`` (requires `entr(1)`_)

Rebuild docs and run server via one terminal: ``make dev_docs``  (requires above, and a 
``make(1)`` with ``-J`` support, e.g. GNU Make)

Formatting / Linting
""""""""""""""""""""
The project uses `black`_ and `isort`_ (one after the other) and runs `flake8`_ via 
CI. See the configuration in `pyproject.toml` and `setup.cfg`:

``make black isort``: Run ``black`` first, then ``isort`` to handle import nuances
``make flake8``, to watch (requires ``entr(1)``): ``make watch_flake8`` 

Releasing
"""""""""
As of 0.1, `poetry`_ handles virtualenv creation, package requirements, versioning,
building, and publishing. Therefore there is no setup.py or requirements files.

Update `__version__` in `__about__.py` and `pyproject.toml`::

	git commit -m 'build(unihan-db): Tag v0.1.1'
	git tag v0.1.1
	git push
	git push --tags
	poetry build
	poetry deploy

.. _cihai: https://cihai.git-pull.com
.. _unihan-etl: https://unihan-etl.git-pull.com
.. _libUnihan: http://libunihan.sourceforge.net/
.. _API: http://unihan-db.git-pull.com/en/latest/api.html
.. _UNIHAN: http://www.unicode.org/charts/unihan.html
.. _poetry: https://python-poetry.org/
.. _entr(1): http://eradman.com/entrproject/
.. _black: https://github.com/psf/black
.. _isort: https://pypi.org/project/isort/
.. _flake8: https://flake8.pycqa.org/

.. |pypi| image:: https://img.shields.io/pypi/v/unihan-db.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/unihan-db

.. |docs| image:: https://github.com/cihai/unihan-db/workflows/Publish%20Docs/badge.svg
   :alt: Docs
   :target: https://github.com/cihai/unihan-db/actions?query=workflow%3A"Publish+Docs"

.. |build-status| image:: https://github.com/cihai/unihan-db/workflows/test/badge.svg
   :alt: Build Status
   :target: https://github.com/cihai/unihan-db/actions?query=workflow%3A"test"

.. |coverage| image:: https://codecov.io/gh/cihai/unihan-db/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/cihai/unihan-db

.. |license| image:: https://img.shields.io/github/license/cihai/unihan-db.svg
    :alt: License 
