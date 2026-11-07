"""unihan_db table schemas.

Tables are split into general categories, similar to how UNIHAN db's files are:

- Unhn_DictionaryIndices
- Unhn_DictionaryLikeData
- Unhn_IRGSources
- Unhn_NumericValues
- Unhn_OtherMappings
- Unhn_RadicalStrokeCounts
- Unhn_Readings
- Unhn_Variants

Tables are prefixed ``Unhn_``, with no vowels.

Those root tables include the base data for all 90 UNIHAN fields. Specialized
values branched off into field-specialized tables through `polymorphic
joins`_.

.. _polymorphic joins: https://en.wikipedia.org/wiki/Polymorphic_association

"""

from __future__ import annotations

import typing as t
from datetime import datetime
from typing import Annotated

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    exists,
    func,
    inspect as sa_inspect,
    select as sa_select,
)
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    class_mapper,
    column_property,
    mapped_column,
    relationship,
)

intpk = Annotated[int, mapped_column(primary_key=True)]
char_fk = Annotated[str, mapped_column(String(1), ForeignKey("Unhn.char"), index=True)]


class Base(DeclarativeBase):
    """SQLAlchemy Declarative base class for UNIHAN DB."""

    def __repr__(self) -> str:
        """Return string representation with primary key columns."""
        mapper = sa_inspect(self.__class__)
        pk_cols = [col.key for col in mapper.primary_key if col.key is not None]
        attrs = ", ".join(f"{k}={getattr(self, k)!r}" for k in pk_cols)
        return f"<{self.__class__.__name__} {attrs}>"

    def to_dict(self, found: set[t.Any] | None = None) -> dict[str, object]:
        """Return dictionary representation of this ORM object.

        Supports recursive relationships.

        Parameters
        ----------
        found : set, optional
            Tracks visited relationships to prevent infinite recursion.

        Returns
        -------
        dict :
            Dictionary representation including columns and relationships.
        """

        def _get_key_value(c: str) -> tuple[str, object]:
            val = getattr(self, c)
            if isinstance(val, datetime):
                return (c, val.isoformat())
            return (c, val)

        found_ = set() if found is None else found

        mapper = class_mapper(self.__class__)
        columns = [column.key for column in mapper.columns]

        result = dict(map(_get_key_value, columns))
        for name, relation in mapper.relationships.items():
            if relation not in found_:
                found_.add(relation)
                related_obj = getattr(self, name)
                if related_obj is not None:
                    if relation.uselist:
                        result[name] = [child.to_dict(found_) for child in related_obj]
                    else:
                        result[name] = related_obj.to_dict(found_)
        return result


class Unhn(Base):
    """Unhn core table."""

    __tablename__ = "Unhn"
    char: Mapped[str] = mapped_column(
        String(1), primary_key=True, index=True, unique=True
    )
    ucn: Mapped[str] = mapped_column(String(8), index=True, unique=True)

    def __repr__(self) -> str:
        """Return string representation with char and ucn."""
        return f"<Unhn char={self.char!r} ucn={self.ucn!r}>"

    @hybrid_property
    def has_definition(self) -> bool:
        """Return True if this character has at least one definition."""
        return len(self.kDefinition) > 0

    @has_definition.inplace.expression
    @classmethod
    def _has_definition_expression(cls) -> t.Any:
        return exists().where(kDefinition.char_id == cls.char)

    @hybrid_property
    def definition_text(self) -> str | None:
        """Return the first definition text, or None."""
        if self.kDefinition:
            return self.kDefinition[0].definition
        return None

    @definition_text.inplace.expression
    @classmethod
    def _definition_text_expression(cls) -> t.Any:
        return (
            sa_select(kDefinition.definition)
            .where(kDefinition.char_id == cls.char)
            .limit(1)
            .correlate(cls)
            .scalar_subquery()
        )

    if t.TYPE_CHECKING:
        definition_count: Mapped[int]

    kDefinition: Mapped[list[kDefinition]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kCantonese: Mapped[list[kCantonese]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kMandarin: Mapped[list[kMandarin]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kTotalStrokes: Mapped[list[kTotalStrokes]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kIRGHanyuDaZidian: Mapped[list[kIRGHanyuDaZidian]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRGDaeJaweon: Mapped[list[kIRGDaeJaweon]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRGKangXi: Mapped[list[kIRGKangXi]] = relationship(
        cascade="all, delete-orphan",
    )
    kHanyuPinyin: Mapped[list[kHanyuPinyin]] = relationship(
        cascade="all, delete-orphan",
    )
    kXHC1983: Mapped[list[kXHC1983]] = relationship(
        cascade="all, delete-orphan",
    )
    kCheungBauer: Mapped[list[kCheungBauer]] = relationship(
        cascade="all, delete-orphan",
    )
    kRSAdobe_Japan1_6: Mapped[list[kRSAdobe_Japan1_6]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kCihaiT: Mapped[list[kCihaiT]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kIICore: Mapped[list[kIICore]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kHanYu: Mapped[list[kHanYu]] = relationship(
        cascade="all, delete-orphan",
    )
    kDaeJaweon: Mapped[list[kDaeJaweon]] = relationship(
        cascade="all, delete-orphan",
    )
    kFenn: Mapped[list[kFenn]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kHanyuPinlu: Mapped[list[kHanyuPinlu]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kHDZRadBreak: Mapped[list[kHDZRadBreak]] = relationship(
        cascade="all, delete-orphan",
    )
    kSBGY: Mapped[list[kSBGY]] = relationship(
        cascade="all, delete-orphan",
    )
    kRSUnicode: Mapped[list[kRSUnicode]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_GSource: Mapped[list[kIRG_GSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_HSource: Mapped[list[kIRG_HSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_JSource: Mapped[list[kIRG_JSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_KPSource: Mapped[list[kIRG_KPSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_KSource: Mapped[list[kIRG_KSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_MSource: Mapped[list[kIRG_MSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_SSource: Mapped[list[kIRG_SSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_TSource: Mapped[list[kIRG_TSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_USource: Mapped[list[kIRG_USource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_UKSource: Mapped[list[kIRG_UKSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kIRG_VSource: Mapped[list[kIRG_VSource]] = relationship(
        cascade="all, delete-orphan",
    )
    kGSR: Mapped[list[kGSR]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )
    kFennIndex: Mapped[list[kFennIndex]] = relationship(
        cascade="all, delete-orphan",
    )
    kCheungBauerIndex: Mapped[list[kCheungBauerIndex]] = relationship(
        cascade="all, delete-orphan",
    )
    kCCCII: Mapped[list[kCCCII]] = relationship(
        back_populates="unhn",
        cascade="all, delete-orphan",
    )


class kCCCII(Base):
    """Table for kCCCII UNIHAN data."""

    __tablename__ = "kCCCII"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    hex: Mapped[str] = mapped_column(String(6))
    unhn: Mapped[Unhn] = relationship(back_populates="kCCCII")


class GenericIRG(Base):
    """Table for Generic IRG UNIHAN data."""

    __tablename__ = "GenericIRG"

    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    source: Mapped[int] = mapped_column()
    location: Mapped[str | None] = mapped_column(String(10))
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {  # noqa: RUF012
        "polymorphic_identity": "generic_irg",
        "polymorphic_on": "type",
    }


class kIRG_GSource(GenericIRG):
    """Table for kIRG_GSource UNIHAN data."""

    __tablename__ = "kIRG_GSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_GSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_HSource(GenericIRG):
    """Table for kIRG_HSource UNIHAN data."""

    __tablename__ = "kIRG_HSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_HSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_JSource(GenericIRG):
    """Table for kIRG_JSource UNIHAN data."""

    __tablename__ = "kIRG_JSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_JSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_KPSource(GenericIRG):
    """Table for kIRG_KPSource UNIHAN data."""

    __tablename__ = "kIRG_KPSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_KPSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_KSource(GenericIRG):
    """Table for kIRG_KSource UNIHAN data."""

    __tablename__ = "kIRG_KSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_KSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_MSource(GenericIRG):
    """Table for kIRG_MSource UNIHAN data."""

    __tablename__ = "kIRG_MSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_MSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_SSource(GenericIRG):
    """Table for kIRG_SSource UNIHAN data."""

    __tablename__ = "kIRG_SSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_SSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_TSource(GenericIRG):
    """Table for kIRG_TSource UNIHAN data."""

    __tablename__ = "kIRG_TSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_TSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_USource(GenericIRG):
    """Table for kIRG_USource UNIHAN data."""

    __tablename__ = "kIRG_USource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_USource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_UKSource(GenericIRG):
    """Table for kIRG_UKSource UNIHAN data."""

    __tablename__ = "kIRG_UKSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_UKSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_VSource(GenericIRG):
    """Table for kIRG_VSource UNIHAN data."""

    __tablename__ = "kIRG_VSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_VSource"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(ForeignKey("GenericIRG.id"), primary_key=True)


class kDefinition(Base):
    """Table for kDefinition UNIHAN data."""

    __tablename__ = "kDefinition"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    definition: Mapped[str] = mapped_column(String(296))
    unhn: Mapped[Unhn] = relationship(back_populates="kDefinition")


Unhn.definition_count = column_property(
    sa_select(func.count(kDefinition.id))
    .where(kDefinition.char_id == Unhn.char)
    .correlate_except(kDefinition)
    .scalar_subquery(),
    deferred=True,
)


class kCantonese(Base):
    """Table for kCantonese UNIHAN data."""

    __tablename__ = "kCantonese"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    definition: Mapped[str] = mapped_column(String(128))
    unhn: Mapped[Unhn] = relationship(back_populates="kCantonese")


class kMandarin(Base):
    """Table for kManadarin UNIHAN data."""

    __tablename__ = "kMandarin"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    hans: Mapped[str] = mapped_column(String(10))
    hant: Mapped[str] = mapped_column(String(10))
    unhn: Mapped[Unhn] = relationship(back_populates="kMandarin")


class kTotalStrokes(Base):
    """Table for kTotalStrokes UNIHAN data."""

    __tablename__ = "kTotalStrokes"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    hans: Mapped[int] = mapped_column()
    hant: Mapped[int] = mapped_column()
    unhn: Mapped[Unhn] = relationship(back_populates="kTotalStrokes")


class GenericReading(Base):
    """Table for GenericReading UNIHAN data."""

    __tablename__ = "GenericReading"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    type: Mapped[str] = mapped_column(String(50))
    locations: Mapped[list[UnhnLocation]] = relationship(
        "UnhnLocation",
        foreign_keys="[UnhnLocation.generic_reading_id]",
        cascade="all, delete-orphan",
    )
    readings: Mapped[list[UnhnReading]] = relationship(
        "UnhnReading",
        cascade="all, delete-orphan",
    )
    reading_strings: AssociationProxy[list[str]] = association_proxy(
        "readings",
        "reading",
    )

    __mapper_args__ = {  # noqa: RUF012
        "polymorphic_identity": "generic_reading",
        "polymorphic_on": "type",
    }


class GenericRadicalStrokes(Base):
    """Table for GenericRadicalStrokes UNIHAN data."""

    __tablename__ = "GenericRadicalStrokes"

    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    radical: Mapped[int] = mapped_column()
    strokes: Mapped[int] = mapped_column()
    simplified: Mapped[str | None] = mapped_column(String(50))
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {  # noqa: RUF012
        "polymorphic_identity": "generic_radical_strokes",
        "polymorphic_on": "type",
    }


class kRSUnicode(GenericRadicalStrokes):
    """Table for kRSUnicode UNIHAN data."""

    __tablename__ = "kRSUnicode"
    __mapper_args__ = {"polymorphic_identity": "kRSUnicode"}  # noqa: RUF012
    id: Mapped[int] = mapped_column(
        ForeignKey("GenericRadicalStrokes.id"),
        primary_key=True,
    )


class kRSAdobe_Japan1_6(Base):
    """Table for kRSAdobe_Japan1_6 UNIHAN data."""

    __tablename__ = "kRSAdobe_Japan1_6"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    type: Mapped[str] = mapped_column(String(1))
    cid: Mapped[int] = mapped_column()
    radical: Mapped[int] = mapped_column()
    strokes: Mapped[int] = mapped_column()
    strokes_residue: Mapped[int] = mapped_column()
    unhn: Mapped[Unhn] = relationship(back_populates="kRSAdobe_Japan1_6")


class kHanyuPinyin(GenericReading):
    """Table for kHanyuPinyin Unihan data."""

    __tablename__ = "kHanyuPinyin"
    __mapper_args__ = {"polymorphic_identity": "kHanyuPinyin"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(
        ForeignKey("GenericReading.id"),
        primary_key=True,
    )


class kXHC1983(GenericReading):
    """Table for kXHC1983 UNIHAN data."""

    __tablename__ = "kXHC1983"
    __mapper_args__ = {"polymorphic_identity": "kXHC1983"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(
        ForeignKey("GenericReading.id"),
        primary_key=True,
    )
    locations: Mapped[list[UnhnLocationkXHC1983]] = relationship(  # type: ignore[assignment]
        "UnhnLocationkXHC1983",
    )


class kCheungBauer(GenericReading):
    """Table for kCheungBauer UNIHAN data."""

    __tablename__ = "kCheungBauer"
    __mapper_args__ = {"polymorphic_identity": "kCheungBauer"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(
        ForeignKey("GenericReading.id"),
        primary_key=True,
    )
    radical: Mapped[int] = mapped_column()
    strokes: Mapped[int] = mapped_column()
    cangjie: Mapped[str | None] = mapped_column(String)


class GenericIndice(Base):
    """Table for GenericIndice UNIHAN data."""

    __tablename__ = "GenericIndice"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    type: Mapped[str] = mapped_column(String(50))
    locations: Mapped[list[UnhnLocation]] = relationship(
        "UnhnLocation",
        foreign_keys="[UnhnLocation.generic_indice_id]",
        cascade="all, delete-orphan",
    )

    __mapper_args__ = {  # noqa: RUF012
        "polymorphic_identity": "generic_indice",
        "polymorphic_on": "type",
    }


class kHanYu(GenericIndice):
    """Table for kHanYu UNIHAN data."""

    __tablename__ = "kHanYu"
    __mapper_args__ = {"polymorphic_identity": "kHanYu"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(ForeignKey("GenericIndice.id"), primary_key=True)


class kIRGHanyuDaZidian(GenericIndice):
    """Table for kIRGHanyuDaZidian UNIHAN data."""

    __tablename__ = "kIRGHanyuDaZidian"
    __mapper_args__ = {"polymorphic_identity": "kIRGHanyuDaZidian"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(ForeignKey("GenericIndice.id"), primary_key=True)


class UnhnLocation(Base):
    """Table for UnhnLocation UNIHAN data."""

    __tablename__ = "UnhnLocation"
    id: Mapped[intpk]
    generic_reading_id: Mapped[int | None] = mapped_column(
        ForeignKey("GenericReading.id"),
        index=True,
    )
    generic_indice_id: Mapped[int | None] = mapped_column(
        ForeignKey("GenericIndice.id"),
        index=True,
    )
    volume: Mapped[int | None] = mapped_column()
    page: Mapped[int] = mapped_column()
    character: Mapped[int] = mapped_column()
    virtual: Mapped[bool | None] = mapped_column(Boolean)


class kCihaiT(Base):
    """Table for kCihaiT UNIHAN data."""

    __tablename__ = "UnhnLocationkCihaiT"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    page: Mapped[int] = mapped_column()
    row: Mapped[int] = mapped_column()
    character: Mapped[int] = mapped_column()
    unhn: Mapped[Unhn] = relationship(back_populates="kCihaiT")


class kIICoreSource(Base):
    """Table for kIICoreSource UIHAN data."""

    __tablename__ = "kIICoreSource"
    id: Mapped[intpk]
    source_id: Mapped[int] = mapped_column(ForeignKey("kIICore.id"), index=True)
    source: Mapped[str] = mapped_column(String(1))
    iicore: Mapped[kIICore] = relationship(back_populates="sources")


class kIICore(Base):
    """Table for kIICore UNIHAN data."""

    __tablename__ = "kIICore"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    priority: Mapped[str] = mapped_column(String(1))
    sources: Mapped[list[kIICoreSource]] = relationship(
        back_populates="iicore",
        cascade="all, delete-orphan",
    )
    unhn: Mapped[Unhn] = relationship(back_populates="kIICore")


class UnhnLocationkXHC1983(Base):
    """Table for UnhnLocationkXHC1983 UNIHAN data."""

    __tablename__ = "UnhnLocationkXHC1983"
    id: Mapped[intpk]
    generic_reading_id: Mapped[int | None] = mapped_column(
        ForeignKey("GenericReading.id"),
        index=True,
    )
    generic_indice_id: Mapped[int | None] = mapped_column(
        ForeignKey("GenericIndice.id"),
        index=True,
    )
    page: Mapped[int] = mapped_column()
    character: Mapped[int] = mapped_column()
    entry: Mapped[int] = mapped_column()
    substituted: Mapped[bool] = mapped_column(Boolean)


class UnhnReading(Base):
    """Table for UnhnReading UNIHAN data."""

    __tablename__ = "UnhnReading"
    id: Mapped[intpk]
    generic_reading_id: Mapped[int] = mapped_column(
        ForeignKey("GenericReading.id"),
        index=True,
    )
    reading: Mapped[str] = mapped_column(String(24))


class kDaeJaweon(GenericIndice):
    """Table for kDaewJaweon UNIHAN data."""

    __tablename__ = "kDaeJaweon"
    __mapper_args__ = {"polymorphic_identity": "kDaeJaweon"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(ForeignKey("GenericIndice.id"), primary_key=True)


class kIRGKangXi(GenericIndice):
    """Table for kIRGKangXi UNIHAN data."""

    __tablename__ = "kIRGKangXi"
    __mapper_args__ = {"polymorphic_identity": "kIRGKangXi"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(ForeignKey("GenericIndice.id"), primary_key=True)


class kIRGDaeJaweon(GenericIndice):
    """Table for kIRGDaeJaweon UNIHAN data."""

    __tablename__ = "kIRGDaeJaweon"
    __mapper_args__ = {"polymorphic_identity": "kIRGDaeJaweon"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(ForeignKey("GenericIndice.id"), primary_key=True)


class kFenn(Base):
    """Table for kFenn UNIHAN data."""

    __tablename__ = "kFenn"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    phonetic: Mapped[str] = mapped_column(String(10))
    frequency: Mapped[str] = mapped_column(String(10))
    unhn: Mapped[Unhn] = relationship(back_populates="kFenn")


class kHanyuPinlu(Base):
    """Table for kHanyuPinlu UNIHAN data."""

    __tablename__ = "kHanyuPinlu"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    phonetic: Mapped[str] = mapped_column(String(10))
    frequency: Mapped[str] = mapped_column(String(10))
    unhn: Mapped[Unhn] = relationship(back_populates="kHanyuPinlu")


class kGSR(Base):
    """Table for kGSR UNIHAN data."""

    __tablename__ = "kGSR"
    id: Mapped[intpk]
    char_id: Mapped[char_fk]
    set: Mapped[int] = mapped_column()
    letter: Mapped[str] = mapped_column(String(1))
    apostrophe: Mapped[bool] = mapped_column(Boolean)
    unhn: Mapped[Unhn] = relationship(back_populates="kGSR")


class kHDZRadBreak(GenericIndice):
    """Table for kHDZRadBreak UNIHAN data."""

    __tablename__ = "kHDZRadBreak"
    __mapper_args__ = {"polymorphic_identity": "kHDZRadBreak"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(ForeignKey("GenericIndice.id"), primary_key=True)
    radical: Mapped[str] = mapped_column(String(10))
    ucn: Mapped[str] = mapped_column(String(10))


class kSBGY(GenericIndice):
    """Table for kSBGY UNIHAN data."""

    __tablename__ = "kSBGY"
    __mapper_args__ = {"polymorphic_identity": "kSBGY"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(ForeignKey("GenericIndice.id"), primary_key=True)


class kCheungBauerIndex(GenericIndice):
    """Table for kCheungBauerIndex UNIHAN data."""

    __tablename__ = "kCheungBauerIndex"
    __mapper_args__ = {"polymorphic_identity": "kCheungBauerIndex"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(ForeignKey("GenericIndice.id"), primary_key=True)


class kFennIndex(GenericIndice):
    """Table for kFennIndex UNIHAN data."""

    __tablename__ = "kFennIndex"
    __mapper_args__ = {"polymorphic_identity": "kFennIndex"}  # noqa: RUF012

    id: Mapped[int] = mapped_column(ForeignKey("GenericIndice.id"), primary_key=True)
