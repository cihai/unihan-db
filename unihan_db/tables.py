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

from sqlalchemy import Base, Column, Integer, String
from sqlalchemy.orm import with_polymorphic


class Unhn(Base):
    __tablename__ = 'Unhn'
    id = Column(Integer, primary_key=True)
    ucn = Column(String(8))
    char = Column(String(1))
    __mapper_args__ = {
        'polymorphic_identity': 'char',
        'polymorphic_on': type
    }


class Unhn_DictionaryIndices(Unhn):
    __table__ = 'Unhn_DictionaryIndices'

    __mapper_args__ = {
        'polymorphic_identity': 'indices',
    }


class Unhn_DictionaryLikeData(Unhn):
    __table__ = 'Unhn_DictionaryLikeData'

    __mapper_args__ = {
        'polymorphic_identity': 'dictionary-like',
    }


class Unhn_IRGSources(Unhn):
    __table__ = 'Unhn_IRGSources'

    __mapper_args__ = {
        'polymorphic_identity': 'irg-sources',
    }


class Unhn_NumericValues(Unhn):
    __table__ = 'Unhn_NumericValues'

    __mapper_args__ = {
        'polymorphic_identity': 'numeric-values',
    }


class Unhn_OtherMappings(Unhn):
    __table__ = 'Unhn_OtherMappings'

    __mapper_args__ = {
        'polymorphic_identity': 'other-mappings',
    }


class Unhn_RadicalStrokeCounts(Unhn):
    __table__ = 'Unhn_RadicalStrokeCounts'

    __mapper_args__ = {
        'polymorphic_identity': 'radical-stroke-counts',
    }


class Unhn_Readings(Unhn):
    __table__ = 'Unhn_Readings'

    __mapper_args__ = {
        'polymorphic_identity': 'readings',
    }


class Unhn_Variants(Unhn):
    __table__ = 'Unhn_Variants'

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
