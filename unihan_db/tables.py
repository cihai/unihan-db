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
from sqlalchemy.orm import relationship


Base = declarative_base()


class Unhn(Base):
    __tablename__ = 'Unhn'
    id = Column(Integer, primary_key=True)
    ucn = Column(String(8))
    char = Column(String(1))
    type = Column(String(24))

    kDefinition = relationship("kDefinition", back_populates="char")


class kDefinition(Base):
    __tablename__ = 'kDefinition'
    id = Column(Integer, primary_key=True)
    char_id = Column(Integer, ForeignKey('Unhn.id'))
    definition = Column(String(128))

    char = relationship("Unhn", back_populates="kDefinition")
