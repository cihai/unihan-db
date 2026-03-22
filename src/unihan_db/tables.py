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

from sqlalchemy import Boolean, ForeignKey, String, inspect as sa_inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """SQLAlchemy Declarative base class for UNIHAN DB."""

    def __repr__(self) -> str:
        """Return string representation with primary key columns."""
        mapper = sa_inspect(self.__class__)
        pk_cols = [col.key for col in mapper.primary_key if col.key is not None]
        attrs = ", ".join(f"{k}={getattr(self, k)!r}" for k in pk_cols)
        return f"<{self.__class__.__name__} {attrs}>"


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

    kDefinition: Mapped[list[kDefinition]] = relationship("kDefinition")
    kCantonese: Mapped[list[kCantonese]] = relationship("kCantonese")
    kMandarin: Mapped[list[kMandarin]] = relationship("kMandarin")
    kTotalStrokes: Mapped[list[kTotalStrokes]] = relationship("kTotalStrokes")
    kIRGHanyuDaZidian: Mapped[list[kIRGHanyuDaZidian]] = relationship(
        "kIRGHanyuDaZidian",
    )
    kIRGDaeJaweon: Mapped[list[kIRGDaeJaweon]] = relationship("kIRGDaeJaweon")
    kIRGKangXi: Mapped[list[kIRGKangXi]] = relationship("kIRGKangXi")
    kHanyuPinyin: Mapped[list[kHanyuPinyin]] = relationship("kHanyuPinyin")
    kXHC1983: Mapped[list[kXHC1983]] = relationship("kXHC1983")
    kCheungBauer: Mapped[list[kCheungBauer]] = relationship("kCheungBauer")
    kRSAdobe_Japan1_6: Mapped[list[kRSAdobe_Japan1_6]] = relationship(
        "kRSAdobe_Japan1_6",
    )
    kCihaiT: Mapped[list[kCihaiT]] = relationship("kCihaiT")
    kIICore: Mapped[list[kIICore]] = relationship("kIICore")
    kHanYu: Mapped[list[kHanYu]] = relationship("kHanYu")
    kDaeJaweon: Mapped[list[kDaeJaweon]] = relationship("kDaeJaweon")
    kFenn: Mapped[list[kFenn]] = relationship("kFenn")
    kHanyuPinlu: Mapped[list[kHanyuPinlu]] = relationship("kHanyuPinlu")
    kHDZRadBreak: Mapped[list[kHDZRadBreak]] = relationship("kHDZRadBreak")
    kSBGY: Mapped[list[kSBGY]] = relationship("kSBGY")
    kRSUnicode: Mapped[list[kRSUnicode]] = relationship("kRSUnicode")
    kIRG_GSource: Mapped[list[kIRG_GSource]] = relationship("kIRG_GSource")
    kIRG_HSource: Mapped[list[kIRG_HSource]] = relationship("kIRG_HSource")
    kIRG_JSource: Mapped[list[kIRG_JSource]] = relationship("kIRG_JSource")
    kIRG_KPSource: Mapped[list[kIRG_KPSource]] = relationship("kIRG_KPSource")
    kIRG_KSource: Mapped[list[kIRG_KSource]] = relationship("kIRG_KSource")
    kIRG_MSource: Mapped[list[kIRG_MSource]] = relationship("kIRG_MSource")
    kIRG_SSource: Mapped[list[kIRG_SSource]] = relationship("kIRG_SSource")
    kIRG_TSource: Mapped[list[kIRG_TSource]] = relationship("kIRG_TSource")
    kIRG_USource: Mapped[list[kIRG_USource]] = relationship("kIRG_USource")
    kIRG_UKSource: Mapped[list[kIRG_UKSource]] = relationship("kIRG_UKSource")
    kIRG_VSource: Mapped[list[kIRG_VSource]] = relationship("kIRG_VSource")
    kGSR: Mapped[list[kGSR]] = relationship("kGSR")
    kFennIndex: Mapped[list[kFennIndex]] = relationship("kFennIndex")
    kCheungBauerIndex: Mapped[list[kCheungBauerIndex]] = relationship(
        "kCheungBauerIndex",
    )
    kCCCII: Mapped[list[kCCCII]] = relationship("kCCCII")


class kCCCII(Base):
    """Table for kCCCII UNIHAN data."""

    __tablename__ = "kCCCII"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    hex: Mapped[str] = mapped_column(String(6))


class GenericIRG(Base):
    """Table for Generic IRG UNIHAN data."""

    __tablename__ = "GenericIRG"

    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(
        String(1),
        ForeignKey("Unhn.char"),
        index=True,
    )
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
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    definition: Mapped[str] = mapped_column(String(296))


class kCantonese(Base):
    """Table for kCantonese UNIHAN data."""

    __tablename__ = "kCantonese"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    definition: Mapped[str] = mapped_column(String(128))


class kMandarin(Base):
    """Table for kManadarin UNIHAN data."""

    __tablename__ = "kMandarin"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    hans: Mapped[str] = mapped_column(String(10))
    hant: Mapped[str] = mapped_column(String(10))


class kTotalStrokes(Base):
    """Table for kTotalStrokes UNIHAN data."""

    __tablename__ = "kTotalStrokes"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    hans: Mapped[int] = mapped_column()
    hant: Mapped[int] = mapped_column()


class GenericReading(Base):
    """Table for GenericReading UNIHAN data."""

    __tablename__ = "GenericReading"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(
        String(1),
        ForeignKey("Unhn.char"),
        index=True,
    )
    type: Mapped[str] = mapped_column(String(50))
    locations: Mapped[list[UnhnLocation]] = relationship("UnhnLocation")
    readings: Mapped[list[UnhnReading]] = relationship("UnhnReading")

    __mapper_args__ = {  # noqa: RUF012
        "polymorphic_identity": "generic_reading",
        "polymorphic_on": "type",
    }


class GenericRadicalStrokes(Base):
    """Table for GenericRadicalStrokes UNIHAN data."""

    __tablename__ = "GenericRadicalStrokes"

    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(
        String(1),
        ForeignKey("Unhn.char"),
        index=True,
    )
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
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    type: Mapped[str] = mapped_column(String(1))
    cid: Mapped[int] = mapped_column()
    radical: Mapped[int] = mapped_column()
    strokes: Mapped[int] = mapped_column()
    strokes_residue: Mapped[int] = mapped_column()


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
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(
        String(1),
        ForeignKey("Unhn.char"),
        index=True,
    )
    type: Mapped[str] = mapped_column(String(50))
    locations: Mapped[list[UnhnLocation]] = relationship("UnhnLocation")

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
    id: Mapped[int] = mapped_column(primary_key=True)
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
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    page: Mapped[int] = mapped_column()
    row: Mapped[int] = mapped_column()
    character: Mapped[int] = mapped_column()


class kIICoreSource(Base):
    """Table for kIICoreSource UIHAN data."""

    __tablename__ = "kIICoreSource"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("kIICore.id"), index=True)
    source: Mapped[str] = mapped_column(String(1))


class kIICore(Base):
    """Table for kIICore UNIHAN data."""

    __tablename__ = "kIICore"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    priority: Mapped[str] = mapped_column(String(1))
    sources: Mapped[list[kIICoreSource]] = relationship("kIICoreSource")


class UnhnLocationkXHC1983(Base):
    """Table for UnhnLocationkXHC1983 UNIHAN data."""

    __tablename__ = "UnhnLocationkXHC1983"
    id: Mapped[int] = mapped_column(primary_key=True)
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
    id: Mapped[int] = mapped_column(primary_key=True)
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
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    phonetic: Mapped[str] = mapped_column(String(10))
    frequency: Mapped[str] = mapped_column(String(10))


class kHanyuPinlu(Base):
    """Table for kHanyuPinlu UNIHAN data."""

    __tablename__ = "kHanyuPinlu"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    phonetic: Mapped[str] = mapped_column(String(10))
    frequency: Mapped[str] = mapped_column(String(10))


class kGSR(Base):
    """Table for kGSR UNIHAN data."""

    __tablename__ = "kGSR"
    id: Mapped[int] = mapped_column(primary_key=True)
    char_id: Mapped[str] = mapped_column(String(1), ForeignKey("Unhn.char"), index=True)
    set: Mapped[int] = mapped_column()
    letter: Mapped[str] = mapped_column(String(1))
    apostrophe: Mapped[bool] = mapped_column(Boolean)


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
