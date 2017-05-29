# -*- coding: utf8 - *-

from unihan_db import bootstrap
from sqlalchemy import MetaData, create_engine


def test_reflect_db(tmpdb_file, unihan_options):
    engine = create_engine('sqlite:///:memory:')
    metadata = MetaData()
    metadata.engine = engine

    assert not bootstrap.is_bootstrapped(metadata)
