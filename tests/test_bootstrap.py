import pathlib
import typing as t

import sqlalchemy
from sqlalchemy.orm import Session
from unihan_db import bootstrap
from unihan_db.tables import Base, Unhn


class UnihanOptions(t.TypedDict):
    source: pathlib.Path
    work_dir: pathlib.Path
    zip_path: pathlib.Path


def test_reflect_db(
    tmpdb_file: pathlib.Path,
    unihan_options: UnihanOptions,
    metadata: sqlalchemy.MetaData,
) -> None:
    assert not bootstrap.is_bootstrapped(metadata)


def test_import_object(session: Session, engine: sqlalchemy.Engine) -> None:
    Base.metadata.create_all(engine)
    session.add(Unhn(char="好", ucn="U+4E09"))
    session.commit()

    assert session.query(Unhn)
    assert session.query(Unhn).count() == 1


def test_import_unihan(
    zip_file: pathlib.Path,
    session: Session,
    engine: sqlalchemy.Engine,
    unihan_options: UnihanOptions,
) -> None:
    Base.metadata.create_all(bind=engine)


def test_import_unihan_raw(
    zip_file: pathlib.Path,
    session: Session,
    engine: sqlalchemy.Engine,
    unihan_options: UnihanOptions,
) -> None:
    Base.metadata.create_all(bind=engine)

    bootstrap.bootstrap_unihan(session, unihan_options)

    session.commit()
