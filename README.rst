*unihan-db* - database sqlalchemy models for `UNIHAN`_. Part of the `cihai`_
project. Powered by `unihan-etl`_. See also: `libUnihan`_.

|pypi| |docs| |build-status| |coverage| |license|

Example usage::

   #!/usr/bin/env python
   # -*- coding: utf8 - *-
   from __future__ import unicode_literals

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

Output::

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

.. _cihai: https://cihai.git-pull.com
.. _unihan-etl: https://unihan-etl.git-pull.com
.. _libUnihan: http://libunihan.sourceforge.net/
.. _API: http://unihan-db.git-pull.com/en/latest/api.html
.. _UNIHAN: http://www.unicode.org/charts/unihan.html

.. |pypi| image:: https://img.shields.io/pypi/v/unihan-db.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/unihan-db

.. |build-status| image:: https://img.shields.io/travis/cihai/unihan-db.svg
   :alt: Build Status
   :target: https://travis-ci.org/cihai/unihan-db

.. |coverage| image:: https://codecov.io/gh/cihai/unihan-db/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/cihai/unihan-db

.. |license| image:: https://img.shields.io/github/license/cihai/unihan-db.svg
    :alt: License 

.. |docs| image:: https://readthedocs.org/projects/unihan-db/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/unihan-db/
