# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

from datetime import datetime

from sqlalchemy import Column, String, Table, create_engine, event
from sqlalchemy.orm import class_mapper, mapper, scoped_session, sessionmaker
from unihan_etl import process as unihan

from . import importer
from .tables import Base, Unhn
from .util import merge_dict

UNIHAN_FILES = [
    'Unihan_DictionaryIndices.txt',
    'Unihan_DictionaryLikeData.txt',
    'Unihan_IRGSources.txt',
    'Unihan_NumericValues.txt',
    'Unihan_RadicalStrokeCounts.txt',
    'Unihan_Readings.txt', 'Unihan_Variants.txt'
]

UNIHAN_FIELDS = [
    'kAccountingNumeric', 'kCangjie', 'kCantonese', 'kCheungBauer',
    'kCihaiT', 'kCompatibilityVariant', 'kDefinition', 'kFenn',
    'kFourCornerCode', 'kFrequency', 'kGradeLevel', 'kHDZRadBreak',
    'kHKGlyph', 'kHangul', 'kHanyuPinlu', 'kHanYu', 'kHanyuPinyin',
    'kJapaneseKun', 'kJapaneseOn', 'kKorean', 'kMandarin',
    'kOtherNumeric', 'kPhonetic', 'kPrimaryNumeric',
    'kRSAdobe_Japan1_6', 'kRSJapanese', 'kRSKanWa', 'kRSKangXi',
    'kRSKorean', 'kRSUnicode', 'kSemanticVariant',
    'kSimplifiedVariant', 'kSpecializedSemanticVariant', 'kTang',
    'kTotalStrokes', 'kTraditionalVariant', 'kVietnamese', 'kXHC1983',
    'kZVariant'
]

UNIHAN_ETL_DEFAULT_OPTIONS = {
    'input_files': UNIHAN_FILES,
    'fields': UNIHAN_FIELDS,
    'format': 'python',
    'expand': True
}


TABLE_NAME = 'Unihan'


DEFAULT_FIELDS = ['ucn', 'char']


def is_bootstrapped(metadata):
    """Return True if cihai is correctly bootstrapped."""
    fields = UNIHAN_FIELDS + DEFAULT_FIELDS
    if TABLE_NAME in metadata.tables.keys():
        table = metadata.tables[TABLE_NAME]

        if set(fields) == set(c.name for c in table.columns):
            return True
        else:
            return False
    else:
        return False


def bootstrap_data(options={}):
    options = merge_dict(UNIHAN_ETL_DEFAULT_OPTIONS.copy(), options)

    p = unihan.Packager(options)
    p.download()
    return p.export()


def bootstrap_unihan(session, options={}):
    """Download, extract and import unihan to database."""
    data = bootstrap_data(options)
    print('bootstrap Unhn table')
    session.bulk_insert_mappings(Unhn, data)
    session.commit()
    print('bootstrap Unhn table finished')
    count = 0
    for char in data:
        c = session.query(Unhn).get(char['char'])
        importer.import_char(c, char)
        count += 1
        print("imported %s: complete %s" % (char['char'], count))
    session.commit()


def to_dict(obj, found=None):
    def _get_key_value(c):
        if isinstance(getattr(obj, c), datetime):
            return (c, getattr(obj, c).isoformat())
        else:
            return (c, getattr(obj, c))

    if found is None:
        found = set()
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]

    result = dict(map(_get_key_value, columns))
    for name, relation in mapper.relationships.items():
        if relation not in found:
            found.add(relation)
            related_obj = getattr(obj, name)
            if related_obj is not None:
                if relation.uselist:
                    result[name] = [
                        to_dict(child, found) for child in related_obj
                    ]
                else:
                    result[name] = to_dict(related_obj, found)
    return result


def add_to_dict(b):
    b.to_dict = to_dict
    return b


def get_session(engine_url='sqlite:///:memory:'):
    engine = create_engine(engine_url)

    event.listen(mapper, 'after_configured', add_to_dict(Base))
    Base.metadata.bind = engine
    Base.metadata.create_all()
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)

    return session


def create_unihan_table(columns, metadata):
    """Create table and return  :class:`sqlalchemy.Table`.

    :param columns: columns for table, i.e. ['kDefinition', 'kCantonese']
    :type columns: list
    :param metadata: Instance of sqlalchemy metadata
    :type metadata: :class:`sqlalchemy.schema.MetaData`
    :returns: Newly created table with columns and index.
    :rtype: :class:`sqlalchemy.schema.Table`

    """

    if TABLE_NAME not in metadata.tables:
        table = Table(TABLE_NAME, metadata)

        table.append_column(Column('char', String(12), primary_key=True))
        table.append_column(Column('ucn', String(12), primary_key=True))

        for column_name in columns:
            col = Column(column_name, String(256), nullable=True)
            table.append_column(col)

        return table
    else:
        return Table(TABLE_NAME, metadata)
