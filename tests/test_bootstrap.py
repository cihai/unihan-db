"""Tests for bootstrapping of UNIHAN."""

from __future__ import annotations

import typing as t

from unihan_db import bootstrap
from unihan_db.tables import Base, Unhn

if t.TYPE_CHECKING:
    import pathlib

    import sqlalchemy
    from sqlalchemy.orm import Session

    from .types import UnihanOptions


def test_reflect_db(
    tmpdb_file: pathlib.Path,
    unihan_options: UnihanOptions,
    metadata: sqlalchemy.MetaData,
) -> None:
    """Test is_bootstrapped()."""
    assert not bootstrap.is_bootstrapped(metadata)


def test_import_object(session: Session, engine: sqlalchemy.Engine) -> None:
    """Test importing and querying of character to Unhn table."""
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
    """Test creation of UNIHAN database."""
    Base.metadata.create_all(bind=engine)


def test_import_unihan_raw(
    zip_file: pathlib.Path,
    session: Session,
    engine: sqlalchemy.Engine,
    unihan_options: UnihanOptions,
) -> None:
    """Test import of UNIHAN data to database."""
    Base.metadata.create_all(bind=engine)

    bootstrap.bootstrap_unihan(session, unihan_options)

    session.commit()
