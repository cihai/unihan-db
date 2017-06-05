# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

from unihan_db.tables import (UnhnLocation, UnhnReading, kCantonese,
                              kDefinition, kHanYu, kHanyuPinyin, kMandarin)


def import_char(c, char):
    if 'kDefinition' in char:
        for defi in char['kDefinition']:
            c.kDefinition.append(kDefinition(definition=defi))
        assert len(c.kDefinition) == len(char['kDefinition'])
    if 'kCantonese' in char:
        for defi in char['kCantonese']:
            c.kCantonese.append(kCantonese(definition=defi))
        assert len(c.kCantonese) == len(char['kCantonese'])
    if 'kMandarin' in char:
        defi = char['kMandarin']
        c.kMandarin.append(kMandarin(
            hans=defi['zh-Hans'],
            hant=defi['zh-Hant'],
        ))

    if 'kHanyuPinyin' in char:
        for defi in char['kHanyuPinyin']:
            k = kHanyuPinyin()
            for loc in defi['locations']:
                k.locations.append(UnhnLocation(
                    volume=loc['volume'],
                    page=loc['page'],
                    character=loc['character'],
                    virtual=loc['virtual'],
                ))
            for reading in defi['readings']:
                k.readings.append(UnhnReading(reading=reading))
            c.kHanyuPinyin.append(k)

    if 'kHanYu' in char:
        for defi in char['kHanYu']:
            k = kHanYu()
            k.locations.append(UnhnLocation(
                volume=defi['volume'],
                page=defi['page'],
                character=defi['character'],
                virtual=defi['virtual'],
            ))
            c.kHanYu.append(k)
