"""Tests for bootstrapping of UNIHAN."""

from __future__ import annotations

import typing as t

from sqlalchemy import func, select

from unihan_db import bootstrap
from unihan_db.tables import Base, Unhn, UnhnReading, kDefinition, kHanyuPinyin

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


def test_has_definition_python(session: Session, engine: sqlalchemy.Engine) -> None:
    """Test has_definition hybrid_property at Python level."""
    Base.metadata.create_all(engine)
    with_def = Unhn(char="水", ucn="U+6C34")
    with_def.kDefinition.append(kDefinition(definition="water"))
    without_def = Unhn(char="火", ucn="U+706B")
    session.add_all([with_def, without_def])
    session.commit()

    assert with_def.has_definition is True
    assert without_def.has_definition is False


def test_has_definition_sql(session: Session, engine: sqlalchemy.Engine) -> None:
    """Test has_definition hybrid_property in SQL WHERE clause."""
    Base.metadata.create_all(engine)
    with_def = Unhn(char="金", ucn="U+91D1")
    with_def.kDefinition.append(kDefinition(definition="gold"))
    without_def = Unhn(char="木", ucn="U+6728")
    session.add_all([with_def, without_def])
    session.commit()

    results = session.scalars(select(Unhn).where(Unhn.has_definition)).all()
    chars = {r.char for r in results}
    assert "金" in chars
    assert "木" not in chars


def test_definition_text(session: Session, engine: sqlalchemy.Engine) -> None:
    """Test definition_text hybrid_property."""
    Base.metadata.create_all(engine)
    char = Unhn(char="土", ucn="U+571F")
    char.kDefinition.append(kDefinition(definition="earth"))
    session.add(char)
    session.commit()

    assert char.definition_text == "earth"

    result = session.scalar(
        select(Unhn.definition_text).where(Unhn.char == "土"),
    )
    assert result == "earth"


def test_definition_count(session: Session, engine: sqlalchemy.Engine) -> None:
    """Test definition_count column_property."""
    Base.metadata.create_all(engine)
    char = Unhn(char="日", ucn="U+65E5")
    char.kDefinition.append(kDefinition(definition="sun"))
    char.kDefinition.append(kDefinition(definition="day"))
    session.add(char)
    session.commit()

    session.expire(char)
    assert char.definition_count == 2


def test_reading_strings_proxy(
    session: Session,
    engine: sqlalchemy.Engine,
) -> None:
    """Test reading_strings association proxy on GenericReading."""
    Base.metadata.create_all(engine)
    char = Unhn(char="月", ucn="U+6708")
    khp = kHanyuPinyin(
        readings=[UnhnReading(reading="yue4")],
    )
    char.kHanyuPinyin.append(khp)
    session.add(char)
    session.commit()

    assert khp.reading_strings == ["yue4"]


def test_lookup_char_full(
    zip_file: object,
    session: Session,
    engine: sqlalchemy.Engine,
    unihan_options: UnihanOptions,
) -> None:
    """Test lookup_char_full() returns character with all relationships."""
    Base.metadata.create_all(bind=engine)
    bootstrap.bootstrap_unihan(session, unihan_options)
    session.commit()

    result = bootstrap.lookup_char_full(session, "好")
    if result is not None:
        assert result.char == "好"
        assert isinstance(result.kDefinition, list)
