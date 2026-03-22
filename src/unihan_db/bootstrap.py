"""Fetch, extract, transform, and load UNIHAN into database."""

from __future__ import annotations

import logging
import typing as t
from collections.abc import Generator
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, scoped_session, selectinload, sessionmaker

from unihan_etl import core as unihan
from unihan_etl.util import merge_dict

from . import dirs, importer
from .tables import Base, Unhn

log = logging.getLogger(__name__)

if t.TYPE_CHECKING:
    from sqlalchemy.orm.scoping import ScopedSession

    from unihan_etl.types import (
        UntypedNormalizedData,
        UntypedUnihanData,
    )


def setup_logger(
    logger: logging.Logger | None = None,
    level: t.Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
) -> None:
    """Configure logging for CLI use.

    Parameters
    ----------
    logger : :py:class:`logging.Logger`
        instance of logger
    level : str
        logging level, e.g. 'INFO'
    """
    if not logger:
        logger = logging.getLogger()
    if not logger.handlers:
        channel = logging.StreamHandler()

        logger.setLevel(level)
        logger.addHandler(channel)


UNIHAN_FILES = (
    "Unihan_DictionaryIndices.txt",
    "Unihan_DictionaryLikeData.txt",
    "Unihan_IRGSources.txt",
    "Unihan_NumericValues.txt",
    "Unihan_RadicalStrokeCounts.txt",
    "Unihan_Readings.txt",
    "Unihan_Variants.txt",
    "Unihan_OtherMappings.txt",
)

UNIHAN_FIELDS = [
    "kAccountingNumeric",
    "kCangjie",
    "kCantonese",
    "kCheungBauer",
    "kCihaiT",
    "kCompatibilityVariant",
    "kDefinition",
    "kFenn",
    "kFourCornerCode",
    "kGradeLevel",
    "kHDZRadBreak",
    "kHKGlyph",
    "kHangul",
    "kHanyuPinlu",
    "kHanYu",
    "kHanyuPinyin",
    "kJapaneseKun",
    "kJapaneseOn",
    "kKorean",
    "kMandarin",
    "kOtherNumeric",
    "kPhonetic",
    "kPrimaryNumeric",
    "kRSAdobe_Japan1_6",
    "kRSUnicode",
    "kSemanticVariant",
    "kSimplifiedVariant",
    "kSpecializedSemanticVariant",
    "kTang",
    "kTotalStrokes",
    "kTraditionalVariant",
    "kVietnamese",
    "kXHC1983",
    "kZVariant",
    "kIICore",
    "kDaeJaweon",
    "kIRGDaeJaweon",
    "kIRGKangXi",
    "kIRG_GSource",
    "kIRG_HSource",
    "kIRG_JSource",
    "kIRG_KPSource",
    "kIRG_KSource",
    "kIRG_MSource",
    "kIRG_SSource",
    "kIRG_TSource",
    "kIRG_USource",
    "kIRG_UKSource",
    "kIRG_VSource",
    "kGSR",
    "kCCCII",
]

UNIHAN_ETL_DEFAULT_OPTIONS = {
    "input_files": UNIHAN_FILES,
    "fields": UNIHAN_FIELDS,
    "format": "python",
    "expand": True,
}


TABLE_NAME = "Unihan"


DEFAULT_FIELDS = ["ucn", "char"]


def is_bootstrapped(metadata: sqlalchemy.MetaData) -> bool:
    """Return True if cihai is correctly bootstrapped."""
    fields = UNIHAN_FIELDS + DEFAULT_FIELDS
    if TABLE_NAME in metadata.tables:
        table = metadata.tables[TABLE_NAME]

        return set(fields) == {c.name for c in table.columns}
    return False


def bootstrap_data(
    options: UntypedUnihanData | None = None,
) -> UntypedNormalizedData | None:
    """Fetch, download, and export UNIHAN data in dictionary format."""
    if options is None:
        options = {}
    options_ = options

    options_ = merge_dict(UNIHAN_ETL_DEFAULT_OPTIONS.copy(), options_)

    p = unihan.Packager(options_)
    p.download()
    return p.export()


def bootstrap_unihan(
    session: Session | ScopedSession[t.Any],
    options: UntypedUnihanData | None = None,
) -> None:
    """Bootstrap UNIHAN to database."""
    options_ = options if options is not None else {}

    if session.scalar(select(func.count()).select_from(Unhn)) == 0:
        data = bootstrap_data(options_)
        assert data is not None
        log.info("bootstrap Unhn table started")
        total_count = len(data)
        items = []

        for count, char in enumerate(data, 1):
            assert isinstance(char, dict)
            c = Unhn(char=char["char"], ucn=char["ucn"])
            importer.import_char(c, char)
            items.append(c)

            if log.isEnabledFor(logging.INFO):
                log.info(
                    "processing %s (%d of %d)",
                    char["char"],
                    count,
                    total_count,
                    extra={
                        "unihan_record_count": count,
                    },
                )

        log.info(
            "adding rows to database",
            extra={"unihan_db_rows": total_count},
        )
        session.add_all(items)
        # This takes a bit of time and doesn't provide progress, but it's by
        # far the fastest way to insert as of SQLAlchemy 1.11.
        session.commit()
        log.info(
            "bootstrap completed",
            extra={"unihan_db_rows": total_count},
        )


def to_dict(obj: t.Any, found: set[t.Any] | None = None) -> dict[str, object]:
    """Return dictionary of an SQLAlchemy Query result.

    Delegates to :meth:`Base.to_dict`. Kept for backward compatibility.

    Parameters
    ----------
    obj : :class:`sqlalchemy.orm.query.Query` result object
        SQLAlchemy Query result
    found : :class:`python:set`
        recursive parameters

    Returns
    -------
    dict :
        dictionary representation of a SQLAlchemy query
    """
    result: dict[str, object] = obj.to_dict(found)
    return result


def get_session(
    engine_url: str = "sqlite:///{user_data_dir}/unihan_db.db",
) -> ScopedSession[t.Any]:
    """Return new SQLAlchemy session object from engine string.

    *engine_url* accepts a string template variable for ``{user_data_dir}``,
    which is replaced to the XDG data directory for the user running the script
    process. This variable is only useful for SQLite, where file paths are
    used for the engine_url.

    Parameters
    ----------
    engine_url : str
        SQLAlchemy engine string
    """
    engine_url = engine_url.format(user_data_dir=dirs.user_data_dir)
    engine = create_engine(engine_url)

    Base.metadata.create_all(bind=engine)
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


@contextmanager
def get_session_context(
    engine_url: str = "sqlite:///{user_data_dir}/unihan_db.db",
) -> Generator[Session, None, None]:
    """Return a context-managed SQLAlchemy session.

    Usage::

        with get_session_context() as session:
            bootstrap_unihan(session)
            result = session.execute(select(Unhn)).scalars().all()

    Parameters
    ----------
    engine_url : str
        SQLAlchemy engine string
    """
    engine_url = engine_url.format(user_data_dir=dirs.user_data_dir)
    engine = create_engine(engine_url)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session


def lookup_char(
    session: Session | ScopedSession[t.Any],
    char: str,
) -> Unhn | None:
    """Look up a character with common fields eagerly loaded.

    Loads kDefinition, kMandarin, kCantonese, and kTotalStrokes via
    selectinload to prevent N+1 queries for common lookup patterns.

    Parameters
    ----------
    session : :class:`~sqlalchemy.orm.Session`
        SQLAlchemy session
    char : str
        Single Unicode character to look up

    Returns
    -------
    :class:`Unhn` or None
        The character row with eagerly loaded fields, or None if not found.
    """
    stmt = (
        select(Unhn)
        .where(Unhn.char == char)
        .options(
            selectinload(Unhn.kDefinition),
            selectinload(Unhn.kMandarin),
            selectinload(Unhn.kCantonese),
            selectinload(Unhn.kTotalStrokes),
        )
    )
    return session.scalar(stmt)
