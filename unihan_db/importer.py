# -*- coding: utf8 - *-
from __future__ import (absolute_import, print_function, unicode_literals,
                        with_statement)

from unihan_db.tables import (UnhnLocation, UnhnLocationkXHC1983, UnhnReading,
                              kCantonese, kCheungBauer, kCihaiT, kDefinition,
                              kHanYu, kHanyuPinyin, kIICore, kIICoreSource,
                              kIRGHanyuDaZidian, kMandarin, kRSAdobe_Japan1_6,
                              kTotalStrokes, kXHC1983)


def import_char(c, char):
    if 'kDefinition' in char:
        for d in char['kDefinition']:
            c.kDefinition.append(kDefinition(definition=d))
    if 'kCantonese' in char:
        for d in char['kCantonese']:
            c.kCantonese.append(kCantonese(definition=d))
    if 'kMandarin' in char:
        d = char['kMandarin']
        c.kMandarin.append(kMandarin(
            hans=d['zh-Hans'],
            hant=d['zh-Hant'],
        ))

    if 'kTotalStrokes' in char:
        d = char['kTotalStrokes']
        c.kTotalStrokes.append(kTotalStrokes(
            hans=d['zh-Hans'],
            hant=d['zh-Hant'],
        ))

    if 'kHanyuPinyin' in char:
        for d in char['kHanyuPinyin']:
            k = kHanyuPinyin()
            for loc in d['locations']:
                k.locations.append(UnhnLocation(
                    volume=loc['volume'],
                    page=loc['page'],
                    character=loc['character'],
                    virtual=loc['virtual'],
                ))
            for reading in d['readings']:
                k.readings.append(UnhnReading(reading=reading))
            c.kHanyuPinyin.append(k)

    if 'kHanYu' in char:
        for d in char['kHanYu']:
            k = kHanYu()
            k.locations.append(UnhnLocation(
                volume=d['volume'],
                page=d['page'],
                character=d['character'],
                virtual=d['virtual'],
            ))
            c.kHanYu.append(k)

    if 'kIRGHanyuDaZidian' in char:
        for d in char['kIRGHanyuDaZidian']:
            k = kIRGHanyuDaZidian()
            k.locations.append(UnhnLocation(
                volume=d['volume'],
                page=d['page'],
                character=d['character'],
                virtual=d['virtual'],
            ))
            c.kIRGHanyuDaZidian.append(k)

    if 'kXHC1983' in char:
        for d in char['kXHC1983']:
            k = kXHC1983()
            for loc in d['locations']:
                k.locations.append(UnhnLocationkXHC1983(
                    page=loc['page'],
                    character=loc['character'],
                    entry=loc['entry'],
                    substituted=loc['substituted'],
                ))
            k.readings.append(UnhnReading(reading=d['reading']))
            c.kXHC1983.append(k)

    if 'kCheungBauer' in char:
        for d in char['kCheungBauer']:
            k = kCheungBauer(
                radical=d['radical'],
                strokes=d['strokes'],
                cangjie=d['cangjie'],
            )

            for reading in d['readings']:
                k.readings.append(UnhnReading(reading=reading))
            c.kCheungBauer.append(k)

    if 'kRSAdobe_Japan1_6' in char:
        for d in char['kRSAdobe_Japan1_6']:
            c.kRSAdobe_Japan1_6.append(kRSAdobe_Japan1_6(
                type=d['type'],
                cid=d['cid'],
                radical=d['radical'],
                strokes=d['strokes'],
                strokes_residue=d['strokes-residue'],
            ))

    if 'kCihaiT' in char:
        for d in char['kCihaiT']:
            c.kCihaiT.append(kCihaiT(
                page=d['page'],
                row=d['row'],
                character=d['character'],
            ))

    if 'kIICore' in char:
        for d in char['kIICore']:
            k = kIICore(priority=d['priority'])
            for s in d['sources']:
                k.sources.append(kIICoreSource(
                    source=s
                ))
            c.kIICore.append(k)
