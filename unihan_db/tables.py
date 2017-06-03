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

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import with_polymorphic

Base = declarative_base()


class Unhn(Base):
    __tablename__ = 'Unhn'
    id = Column(Integer, primary_key=True)
    ucn = Column(String(8))
    char = Column(String(1))
    type = Column(String(24))
    __mapper_args__ = {
        'polymorphic_identity': 'char',
        'polymorphic_on': 'type'
    }


class Unhn_DictionaryIndices(Unhn):
    __tablename__ = 'Unhn_DictionaryIndices'

    unhn_id = Column(Integer, ForeignKey('Unhn.id'))
    definition = Column(String(8))

    __mapper_args__ = {
        'polymorphic_identity': 'indices',
    }


class Unhn_DictionaryLikeData(Unhn):
    __tablename__ = 'Unhn_DictionaryLikeData'
    unhn_id = Column(Integer, ForeignKey('Unhn.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'dictionary-like',
    }


class Unhn_IRGSources(Unhn):
    __tablename__ = 'Unhn_IRGSources'
    unhn_id = Column(Integer, ForeignKey('Unhn.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'irg-sources',
    }


class Unhn_NumericValues(Unhn):
    __tablename__ = 'Unhn_NumericValues'
    unhn_id = Column(Integer, ForeignKey('Unhn.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'numeric-values',
    }


class Unhn_OtherMappings(Unhn):
    __tablename__ = 'Unhn_OtherMappings'
    unhn_id = Column(Integer, ForeignKey('Unhn.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'other-mappings',
    }


class Unhn_RadicalStrokeCounts(Unhn):
    __tablename__ = 'Unhn_RadicalStrokeCounts'
    unhn_id = Column(Integer, ForeignKey('Unhn.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'radical-stroke-counts',
    }


class Unhn_Readings(Unhn):
    __tablename__ = 'Unhn_Readings'
    unhn_id = Column(Integer, ForeignKey('Unhn.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'readings',
    }


class Unhn_Variants(Unhn):
    __tablename__ = 'Unhn_Variants'
    unhn_id = Column(Integer, ForeignKey('Unhn.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'variants',
    }


query = with_polymorphic(Unhn, [
    Unhn_DictionaryIndices,
    Unhn_DictionaryLikeData,
    Unhn_IRGSources,
    Unhn_NumericValues,
    Unhn_OtherMappings,
    Unhn_RadicalStrokeCounts,
    Unhn_Readings,
    Unhn_Variants
])
