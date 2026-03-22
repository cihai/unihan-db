"""Tests for bootstrapping of UNIHAN."""

from __future__ import annotations

import typing as t

from sqlalchemy import func, select

from unihan_db import bootstrap
from unihan_db.tables import Base, Unhn, kDefinition

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

    assert session.execute(select(Unhn)).scalars().first() is not None
    assert session.scalar(select(func.count()).select_from(Unhn)) == 1


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


def test_unhn_repr(session: Session, engine: sqlalchemy.Engine) -> None:
    """Test __repr__ on Unhn model."""
    Base.metadata.create_all(engine)
    char = Unhn(char="大", ucn="U+5927")
    session.add(char)
    session.commit()

    assert repr(char) == "<Unhn char='大' ucn='U+5927'>"


def test_base_repr(session: Session, engine: sqlalchemy.Engine) -> None:
    """Test generic __repr__ on child model."""
    Base.metadata.create_all(engine)
    char = Unhn(char="中", ucn="U+4E2D")
    defn = kDefinition(definition="middle")
    char.kDefinition.append(defn)
    session.add(char)
    session.commit()

    assert "<kDefinition id=" in repr(defn)


def test_to_dict(session: Session, engine: sqlalchemy.Engine) -> None:
    """Test Base.to_dict() method."""
    Base.metadata.create_all(engine)
    char = Unhn(char="人", ucn="U+4EBA")
    defn = kDefinition(definition="person")
    char.kDefinition.append(defn)
    session.add(char)
    session.commit()

    result = char.to_dict()
    assert result["char"] == "人"
    assert result["ucn"] == "U+4EBA"
    assert isinstance(result["kDefinition"], list)
    assert len(result["kDefinition"]) == 1
    assert result["kDefinition"][0]["definition"] == "person"


def test_to_dict_compat(session: Session, engine: sqlalchemy.Engine) -> None:
    """Test backward-compatible bootstrap.to_dict() wrapper."""
    Base.metadata.create_all(engine)
    char = Unhn(char="天", ucn="U+5929")
    session.add(char)
    session.commit()

    result = bootstrap.to_dict(char)
    assert result["char"] == "天"
    assert result["ucn"] == "U+5929"
