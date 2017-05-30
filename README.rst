*unihan-db* - database sqlalchemy models for `UNIHAN`_. Part of the `cihai`_
project. Powered by `unihan-etl`_. See also: `libUnihan`_.

|pypi| |docs| |build-status| |coverage| |license|

There is no clear solution for normalization of UNIHAN.

Approaches
----------

5nf
"""

Pros:

- Most portable, it'd be possible to offer an sqlite file dump to make
  data available a la carte

Cons:

- Giving each field a table of its own would comprise over 90 tables, making
  JOIN's impossible in a single query on MySQL (limit on joins is 61).

Polymorphic
"""""""""""

Tables could be branched by grouping fields into "types", just like UNIHAN
db groups fields into files.

http://docs.sqlalchemy.org/en/latest/orm/inheritance.html

Links
-----

* `API`_

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
