# -*- coding: utf8 - *-

from unihan_db import bootstrap
from unihan_db.tables import Unhn, Base


def test_reflect_db(tmpdb_file, unihan_options, metadata):
    assert not bootstrap.is_bootstrapped(metadata)


def test_import(session, engine):
    Base.metadata.create_all(engine)
    session.add(Unhn(char=u'好', ucn='U+4E09'))
    session.commit()

    assert session.query(Unhn)
    assert session.query(Unhn).count() == 1
