# -*- coding: utf8 - *-

from unihan_db import bootstrap


def test_reflect_db(tmpdb_file, unihan_options, metadata):
    assert not bootstrap.is_bootstrapped(metadata)
