# -*- coding: utf8 - *-

from unihan_db import bootstrap
from unihan_db.tables import Unhn, kDefinition, Base


def test_reflect_db(tmpdb_file, unihan_options, metadata):
    assert not bootstrap.is_bootstrapped(metadata)


def test_import_object(session, engine):
    Base.metadata.create_all(engine)
    session.add(Unhn(char=u'好', ucn='U+4E09'))
    session.commit()

    assert session.query(Unhn)
    assert session.query(Unhn).count() == 1


def test_import_unihan(zip_file, session, engine, unihan_options):
    Base.metadata.bind = engine
    Base.metadata.create_all()
    bootstrap.bootstrap_unihan(Base.metadata, unihan_options)


def test_import_unihan_raw(zip_file, session, engine, unihan_options):
    Base.metadata.bind = engine
    Base.metadata.create_all()

    data = bootstrap.bootstrap_data(unihan_options)

    session.bulk_insert_mappings(Unhn, data)
    session.commit()

    assert session.query(Unhn).count() == len(data)

    assert session.query(Unhn).filter_by(char=u'㐀').one().ucn == 'U+3400'

    for char in data:
        if 'kDefinition' in char and char['kDefinition']:
            c = session.query(Unhn).filter_by(ucn=char['ucn']).one()
            for defi in char['kDefinition'].split(' '):
                c.kDefinition.append(kDefinition(definition=defi))
    session.commit()
