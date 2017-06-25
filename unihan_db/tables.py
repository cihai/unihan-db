# -*- coding: utf8 - *-
"""
unihan_db table design
----------------------

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
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Unhn(Base):
    __tablename__ = 'Unhn'
    char = Column(String(1), primary_key=True, index=True, unique=True)
    ucn = Column(String(8), index=True, unique=True)

    kDefinition = relationship("kDefinition")
    kCantonese = relationship("kCantonese")
    kMandarin = relationship("kMandarin")
    kTotalStrokes = relationship("kTotalStrokes")
    kIRGHanyuDaZidian = relationship("kIRGHanyuDaZidian")
    kHanyuPinyin = relationship("kHanyuPinyin")
    kHanYu = relationship("kHanYu")


class kDefinition(Base):
    __tablename__ = 'kDefinition'
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey('Unhn.char'))
    definition = Column(String(296))


class kCantonese(Base):
    __tablename__ = 'kCantonese'
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey('Unhn.char'))
    definition = Column(String(128))


class kMandarin(Base):
    __tablename__ = 'kMandarin'
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey('Unhn.char'))
    hans = Column(String(10))
    hant = Column(String(10))


class kTotalStrokes(Base):
    __tablename__ = 'kTotalStrokes'
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey('Unhn.char'))
    hans = Column(Integer())
    hant = Column(Integer())


class GenericReading(Base):
    __tablename__ = 'GenericReading'
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey('Unhn.char'))
    type = Column(String(50))
    locations = relationship("UnhnLocation")
    readings = relationship("UnhnReading")

    __mapper_args__ = {
        'polymorphic_identity': 'generic_reading',
        'polymorphic_on': type
    }


class kHanyuPinyin(GenericReading):
    __tablename__ = 'kHanyuPinyin'
    __mapper_args__ = {
        'polymorphic_identity': 'kHanyuPinyin',
    }

    id = Column(Integer, ForeignKey('GenericReading.id'), primary_key=True)


class GenericIndice(Base):
    __tablename__ = 'GenericIndice'
    id = Column(Integer, primary_key=True)
    char_id = Column(String(1), ForeignKey('Unhn.char'))
    type = Column(String(50))
    locations = relationship("UnhnLocation")

    __mapper_args__ = {
        'polymorphic_identity': 'generic_indice',
        'polymorphic_on': type
    }


class kHanYu(GenericIndice):
    __tablename__ = 'kHanYu'
    __mapper_args__ = {
        'polymorphic_identity': 'kHanYu',
    }

    id = Column(Integer, ForeignKey('GenericIndice.id'), primary_key=True)


class kIRGHanyuDaZidian(GenericIndice):
    __tablename__ = 'kIRGHanyuDaZidian'
    __mapper_args__ = {
        'polymorphic_identity': 'kIRGHanyuDaZidian',
    }

    id = Column(Integer, ForeignKey('GenericIndice.id'), primary_key=True)


class UnhnLocation(Base):
    __tablename__ = 'UnhnLocation'
    id = Column(Integer, primary_key=True)
    generic_reading_id = Column(Integer, ForeignKey('GenericReading.id'))
    generic_indice_id = Column(Integer, ForeignKey('GenericIndice.id'))
    volume = Column(Integer)
    page = Column(Integer)
    character = Column(Integer)
    virtual = Column(Integer)


class UnhnReading(Base):
    __tablename__ = 'UnhnReading'
    id = Column(Integer, primary_key=True)
    generic_reading_id = Column(Integer, ForeignKey('GenericReading.id'))
    reading = Column(String(24))
