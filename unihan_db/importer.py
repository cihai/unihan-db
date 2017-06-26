# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

from unihan_db.tables import (UnhnLocation, UnhnLocationkXHC1983, UnhnReading,
                              kCantonese, kCheungBauer, kCihaiT, kDefinition,
                              kHanYu, kHanyuPinyin, kIRGHanyuDaZidian,
                              kMandarin, kRSAdobe_Japan1_6, kTotalStrokes,
                              kXHC1983)


def import_char(c, char):
    if 'kDefinition' in char:
        for defi in char['kDefinition']:
            c.kDefinition.append(kDefinition(definition=defi))
    if 'kCantonese' in char:
        for defi in char['kCantonese']:
            c.kCantonese.append(kCantonese(definition=defi))
    if 'kMandarin' in char:
        defi = char['kMandarin']
        c.kMandarin.append(kMandarin(
            hans=defi['zh-Hans'],
            hant=defi['zh-Hant'],
        ))

    if 'kTotalStrokes' in char:
        defi = char['kTotalStrokes']
        c.kTotalStrokes.append(kTotalStrokes(
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

    if 'kIRGHanyuDaZidian' in char:
        for defi in char['kIRGHanyuDaZidian']:
            k = kIRGHanyuDaZidian()
            k.locations.append(UnhnLocation(
                volume=defi['volume'],
                page=defi['page'],
                character=defi['character'],
                virtual=defi['virtual'],
            ))
            c.kIRGHanyuDaZidian.append(k)

    if 'kXHC1983' in char:
        for defi in char['kXHC1983']:
            k = kXHC1983()
            for loc in defi['locations']:
                k.locations.append(UnhnLocationkXHC1983(
                    page=loc['page'],
                    character=loc['character'],
                    entry=loc['entry'],
                    substituted=loc['substituted'],
                ))
            k.readings.append(UnhnReading(reading=defi['reading']))
            c.kXHC1983.append(k)

    if 'kCheungBauer' in char:
        for defi in char['kCheungBauer']:
            k = kCheungBauer(
                radical=defi['radical'],
                strokes=defi['strokes'],
                cangjie=defi['cangjie'],
            )

            for reading in defi['readings']:
                k.readings.append(UnhnReading(reading=reading))
            c.kCheungBauer.append(k)

    if 'kRSAdobe_Japan1_6' in char:
        for defi in char['kRSAdobe_Japan1_6']:
            c.kRSAdobe_Japan1_6.append(kRSAdobe_Japan1_6(
                type=defi['type'],
                cid=defi['cid'],
                radical=defi['radical'],
                strokes=defi['strokes'],
                strokes_residue=defi['strokes-residue'],
            ))

    if 'kCihaiT' in char:
        for defi in char['kCihaiT']:
            c.kCihaiT.append(kCihaiT(
                page=defi['page'],
                row=defi['row'],
                character=defi['character'],
            ))
