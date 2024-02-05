# ruff: noqa: RUF012
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
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """SQLAlchemy Declarative base class for UNIHAN DB."""

    pass


class Unhn(Base):
    """Unhn core table."""

    __tablename__ = "Unhn"
    char = Column(String(1), primary_key=True, index=True, unique=True)
    ucn = Column(String(8), index=True, unique=True)

    kDefinition = relationship("kDefinition")
    kCantonese = relationship("kCantonese")
    kMandarin = relationship("kMandarin")
    kTotalStrokes = relationship("kTotalStrokes")
    kIRGHanyuDaZidian = relationship("kIRGHanyuDaZidian")
    kIRGDaeJaweon = relationship("kIRGDaeJaweon")
    kIRGKangXi = relationship("kIRGKangXi")
    kHanyuPinyin = relationship("kHanyuPinyin")
    kXHC1983 = relationship("kXHC1983")
    kCheungBauer = relationship("kCheungBauer")
    kRSAdobe_Japan1_6 = relationship("kRSAdobe_Japan1_6")
    kCihaiT = relationship("kCihaiT")
    kIICore = relationship("kIICore")
    kHanYu = relationship("kHanYu")
    kDaeJaweon = relationship("kDaeJaweon")
    kFenn = relationship("kFenn")
    kHanyuPinlu = relationship("kHanyuPinlu")
    kHDZRadBreak = relationship("kHDZRadBreak")
    kSBGY = relationship("kSBGY")
    kRSUnicode = relationship("kRSUnicode")
    kIRG_GSource = relationship("kIRG_GSource")
    kIRG_HSource = relationship("kIRG_HSource")
    kIRG_JSource = relationship("kIRG_JSource")
    kIRG_KPSource = relationship("kIRG_KPSource")
    kIRG_KSource = relationship("kIRG_KSource")
    kIRG_MSource = relationship("kIRG_MSource")
    kIRG_SSource = relationship("kIRG_SSource")
    kIRG_TSource = relationship("kIRG_TSource")
    kIRG_USource = relationship("kIRG_USource")
    kIRG_UKSource = relationship("kIRG_UKSource")
    kIRG_VSource = relationship("kIRG_VSource")
    kGSR = relationship("kGSR")
    kFennIndex = relationship("kFennIndex")
    kCheungBauerIndex = relationship("kCheungBauerIndex")
    kCCCII = relationship("kCCCII")


class kCCCII(Base):
    """Table for kCCCII UNIHAN data."""

    __tablename__ = "kCCCII"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    hex = Column(String(6))


class GenericIRG(Base):
    """Table for Generic IRG UNIHAN data."""

    __tablename__ = "GenericIRG"

    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    source = Column(Integer)
    location = Column(String(10), nullable=True)
    type = Column(String(50))

    __mapper_args__ = {"polymorphic_identity": "generic_irg", "polymorphic_on": type}


class kIRG_GSource(GenericIRG):
    """Table for kIRG_GSource UNIHAN data."""

    __tablename__ = "kIRG_GSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_GSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_HSource(GenericIRG):
    """Table for kIRG_HSource UNIHAN data."""

    __tablename__ = "kIRG_HSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_HSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_JSource(GenericIRG):
    """Table for kIRG_JSource UNIHAN data."""

    __tablename__ = "kIRG_JSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_JSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_KPSource(GenericIRG):
    """Table for kIRG_KPSource UNIHAN data."""

    __tablename__ = "kIRG_KPSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_KPSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_KSource(GenericIRG):
    """Table for kIRG_KSource UNIHAN data."""

    __tablename__ = "kIRG_KSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_KSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_MSource(GenericIRG):
    """Table for kIRG_MSource UNIHAN data."""

    __tablename__ = "kIRG_MSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_MSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_SSource(GenericIRG):
    """Table for kIRG_SSource UNIHAN data."""

    __tablename__ = "kIRG_SSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_SSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_TSource(GenericIRG):
    """Table for kIRG_TSource UNIHAN data."""

    __tablename__ = "kIRG_TSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_TSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_USource(GenericIRG):
    """Table for kIRG_USource UNIHAN data."""

    __tablename__ = "kIRG_USource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_USource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_UKSource(GenericIRG):
    """Table for kIRG_UKSource UNIHAN data."""

    __tablename__ = "kIRG_UKSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_UKSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kIRG_VSource(GenericIRG):
    """Table for kIRG_VSource UNIHAN data."""

    __tablename__ = "kIRG_VSource"
    __mapper_args__ = {"polymorphic_identity": "kIRG_VSource"}
    id = Column(Integer, ForeignKey("GenericIRG.id"), primary_key=True)


class kDefinition(Base):
    """Table for kDefinition UNIHAN data."""

    __tablename__ = "kDefinition"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    definition = Column(String(296))


class kCantonese(Base):
    """Table for kCantonese UNIHAN data."""

    __tablename__ = "kCantonese"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    definition = Column(String(128))


class kMandarin(Base):
    """Table for kManadarin UNIHAN data."""

    __tablename__ = "kMandarin"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    hans = Column(String(10))
    hant = Column(String(10))


class kTotalStrokes(Base):
    """Table for kTotalStrokes UNIHAN data."""

    __tablename__ = "kTotalStrokes"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    hans = Column(Integer())
    hant = Column(Integer())


class GenericReading(Base):
    """Table for GenericReading UNIHAN data."""

    __tablename__ = "GenericReading"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    type = Column(String(50))
    locations = relationship("UnhnLocation")
    readings = relationship("UnhnReading")

    __mapper_args__ = {
        "polymorphic_identity": "generic_reading",
        "polymorphic_on": type,
    }


class GenericRadicalStrokes(Base):
    """Table for GenericRadicalStrokes UNIHAN data."""

    __tablename__ = "GenericRadicalStrokes"

    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    radical = Column(Integer)
    strokes = Column(Integer)
    simplified = Column(Boolean, nullable=True)
    type = Column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "generic_radical_strokes",
        "polymorphic_on": type,
    }


class kRSUnicode(GenericRadicalStrokes):
    """Table for kRSUnicode UNIHAN data."""

    __tablename__ = "kRSUnicode"
    __mapper_args__ = {"polymorphic_identity": "kRSUnicode"}
    id = Column(Integer, ForeignKey("GenericRadicalStrokes.id"), primary_key=True)


class kRSAdobe_Japan1_6(Base):
    """Table for kRSAdobe_Japan1_6 UNIHAN data."""

    __tablename__ = "kRSAdobe_Japan1_6"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    type = Column(String(1))
    cid = Column(Integer)
    radical = Column(Integer)
    strokes = Column(Integer)
    strokes_residue = Column(Integer)


class kHanyuPinyin(GenericReading):
    """Table for kHanyuPinyin Unihan data."""

    __tablename__ = "kHanyuPinyin"
    __mapper_args__ = {"polymorphic_identity": "kHanyuPinyin"}

    id = Column(Integer, ForeignKey("GenericReading.id"), primary_key=True)


class kXHC1983(GenericReading):
    """Table for kXHC1983 UNIHAN data."""

    __tablename__ = "kXHC1983"
    __mapper_args__ = {"polymorphic_identity": "kXHC1983"}

    id = Column(Integer, ForeignKey("GenericReading.id"), primary_key=True)
    locations = relationship("UnhnLocationkXHC1983")


class kCheungBauer(GenericReading):
    """Table for kCheungBauer UNIHAN data."""

    __tablename__ = "kCheungBauer"
    __mapper_args__ = {"polymorphic_identity": "kCheungBauer"}

    id = Column(Integer, ForeignKey("GenericReading.id"), primary_key=True)
    radical = Column(Integer)
    strokes = Column(Integer)
    cangjie = Column(String, nullable=True)


class GenericIndice(Base):
    """Table for GenericIndice UNIHAN data."""

    __tablename__ = "GenericIndice"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    type = Column(String(50))
    locations = relationship("UnhnLocation")

    __mapper_args__ = {"polymorphic_identity": "generic_indice", "polymorphic_on": type}


class kHanYu(GenericIndice):
    """Table for kHanYu UNIHAN data."""

    __tablename__ = "kHanYu"
    __mapper_args__ = {"polymorphic_identity": "kHanYu"}

    id = Column(Integer, ForeignKey("GenericIndice.id"), primary_key=True)


class kIRGHanyuDaZidian(GenericIndice):
    """Table for kIRGHanyuDaZidian UNIHAN data."""

    __tablename__ = "kIRGHanyuDaZidian"
    __mapper_args__ = {"polymorphic_identity": "kIRGHanyuDaZidian"}

    id = Column(Integer, ForeignKey("GenericIndice.id"), primary_key=True)


class UnhnLocation(Base):
    """Table for UnhnLocation UNIHAN data."""

    __tablename__ = "UnhnLocation"
    id = Column(Integer, primary_key=True)
    generic_reading_id = Column(Integer, ForeignKey("GenericReading.id"))
    generic_indice_id = Column(Integer, ForeignKey("GenericIndice.id"))
    volume = Column(Integer, nullable=True)
    page = Column(Integer)
    character = Column(Integer)
    virtual = Column(Integer, nullable=True)


class kCihaiT(Base):
    """Table for kCihaiT UNIHAN data."""

    __tablename__ = "UnhnLocationkCihaiT"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    page = Column(Integer)
    row = Column(Integer)
    character = Column(Integer)


class kIICoreSource(Base):
    """Table for kIICoreSource UIHAN data."""

    __tablename__ = "kIICoreSource"
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("kIICore.id"))
    source = Column(String(1))


class kIICore(Base):
    """Table for kIICore UNIHAN data."""

    __tablename__ = "kIICore"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    priority = Column(String(1))
    sources = relationship("kIICoreSource")


class UnhnLocationkXHC1983(Base):
    """Table for UnhnLocationkXHC1983 UNIHAN data."""

    __tablename__ = "UnhnLocationkXHC1983"
    id = Column(Integer, primary_key=True)
    generic_reading_id = Column(Integer, ForeignKey("GenericReading.id"))
    generic_indice_id = Column(Integer, ForeignKey("GenericIndice.id"))
    page = Column(Integer)
    character = Column(Integer)
    entry = Column(Integer)
    substituted = Column(Boolean)


class UnhnReading(Base):
    """Table for UnhnReading UNIHAN data."""

    __tablename__ = "UnhnReading"
    id = Column(Integer, primary_key=True)
    generic_reading_id = Column(Integer, ForeignKey("GenericReading.id"))
    reading = Column(String(24))


class kDaeJaweon(GenericIndice):
    """Table for kDaewJaweon UNIHAN data."""

    __tablename__ = "kDaeJaweon"
    __mapper_args__ = {"polymorphic_identity": "kDaeJaweon"}

    id = Column(Integer, ForeignKey("GenericIndice.id"), primary_key=True)


class kIRGKangXi(GenericIndice):
    """Table for kIRGKangXi UNIHAN data."""

    __tablename__ = "kIRGKangXi"
    __mapper_args__ = {"polymorphic_identity": "kIRGKangXi"}

    id = Column(Integer, ForeignKey("GenericIndice.id"), primary_key=True)


class kIRGDaeJaweon(GenericIndice):
    """Table for kIRGDaeJaweon UNIHAN data."""

    __tablename__ = "kIRGDaeJaweon"
    __mapper_args__ = {"polymorphic_identity": "kIRGDaeJaweon"}

    id = Column(Integer, ForeignKey("GenericIndice.id"), primary_key=True)


class kFenn(Base):
    """Table for kFenn UNIHAN data."""

    __tablename__ = "kFenn"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    phonetic = Column(String(10))
    frequency = Column(String(10))


class kHanyuPinlu(Base):
    """Table for kHanyuPinlu UNIHAN data."""

    __tablename__ = "kHanyuPinlu"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    phonetic = Column(String(10))
    frequency = Column(String(10))


class kGSR(Base):
    """Table for kGSR UNIHAN data."""

    __tablename__ = "kGSR"
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey("Unhn.char"))
    set = Column(Integer)
    letter = Column(String(1))
    apostrophe = Column(Boolean)


class kHDZRadBreak(GenericIndice):
    """Table for kHDZRadBreak UNIHAN data."""

    __tablename__ = "kHDZRadBreak"
    __mapper_args__ = {"polymorphic_identity": "kHDZRadBreak"}

    id = Column(Integer, ForeignKey("GenericIndice.id"), primary_key=True)
    radical = Column(String(10))
    ucn = Column(String(10))


class kSBGY(GenericIndice):
    """Table for kSBGY UNIHAN data."""

    __tablename__ = "kSBGY"
    __mapper_args__ = {"polymorphic_identity": "kSBGY"}

    id = Column(Integer, ForeignKey("GenericIndice.id"), primary_key=True)


class kCheungBauerIndex(GenericIndice):
    """Table for kCheungBauerIndex UNIHAN data."""

    __tablename__ = "kCheungBauerIndex"
    __mapper_args__ = {"polymorphic_identity": "kCheungBauerIndex"}

    id = Column(Integer, ForeignKey("GenericIndice.id"), primary_key=True)


class kFennIndex(GenericIndice):
    """Table for kFennIndex UNIHAN data."""

    __tablename__ = "kFennIndex"
    __mapper_args__ = {"polymorphic_identity": "kFennIndex"}

    id = Column(Integer, ForeignKey("GenericIndice.id"), primary_key=True)
