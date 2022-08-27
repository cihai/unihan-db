import typing as t
import zipfile

import pytest

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.schema import MetaData

from unihan_db import bootstrap
from unihan_db.tables import Base, Unhn

from .conftest import UnihanTestOptions


@pytest.mark.usefixtures("tmpdb_file")
def test_reflect_db(unihan_options: UnihanTestOptions, metadata: MetaData) -> None:
    assert not bootstrap.is_bootstrapped(metadata)


def test_import_object(session: Session, engine: Engine) -> None:
    Base.metadata.create_all(engine)
    session.add(Unhn(char="好", ucn="U+4E09"))
    session.commit()

    assert session.query(Unhn)
    assert session.query(Unhn).count() == 1


def test_import_unihan(
    zip_file: zipfile.ZipFile,
    session: Session,
    engine: Engine,
    unihan_options: UnihanTestOptions,
) -> None:
    Base.metadata.bind = engine
    Base.metadata.create_all()
    # bootstrap.bootstrap_unihan(Base.metadata, unihan_options)


def test_import_unihan_raw(
    zip_file: zipfile.ZipFile,
    session: ScopedSession,
    engine: Engine,
    unihan_options: t.Dict[str, t.Union[str, bool]],
) -> None:
    Base.metadata.bind = engine
    Base.metadata.create_all()

    bootstrap.bootstrap_unihan(session, unihan_options)

    session.commit()
