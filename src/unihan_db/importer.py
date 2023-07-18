# flake8: noqa: PERF401
import typing as t

from unihan_db.tables import (
    Unhn,
    UnhnLocation,
    UnhnLocationkXHC1983,
    UnhnReading,
    kCantonese,
    kCCCII,
    kCheungBauer,
    kCheungBauerIndex,
    kCihaiT,
    kDaeJaweon,
    kDefinition,
    kFenn,
    kFennIndex,
    kGSR,
    kHanYu,
    kHanyuPinlu,
    kHanyuPinyin,
    kHDZRadBreak,
    kIICore,
    kIICoreSource,
    kIRG_GSource,
    kIRG_HSource,
    kIRG_JSource,
    kIRG_KPSource,
    kIRG_KSource,
    kIRG_MSource,
    kIRG_TSource,
    kIRG_USource,
    kIRG_VSource,
    kIRGDaeJaweon,
    kIRGHanyuDaZidian,
    kIRGKangXi,
    kMandarin,
    kRSAdobe_Japan1_6,
    kRSJapanese,
    kRSKangXi,
    kRSKanWa,
    kRSKorean,
    kRSUnicode,
    kSBGY,
    kTotalStrokes,
    kXHC1983,
)


def import_char(
    c: Unhn,
    char: t.Dict[
        str,
        t.Union[
            t.Dict[
                str,
                t.Union[int, str, t.List[t.Dict[str, object]], t.Dict[str, object]],
            ],
            t.List[t.Dict[str, object]],
            t.Dict[str, object],
        ],
    ],
) -> None:
    if "kDefinition" in char:
        for kd in char["kDefinition"]:
            c.kDefinition.append(kDefinition(definition=kd))
    if "kCantonese" in char:
        for kc in char["kCantonese"]:
            c.kCantonese.append(kCantonese(definition=kc))
    if "kCCCII" in char:
        for kci in char["kCCCII"]:
            assert isinstance(kci, dict)
            c.kCCCII.append(kCCCII(hex=kci))
    if "kMandarin" in char:
        km = char["kMandarin"]
        assert isinstance(km, dict)
        c.kMandarin.append(kMandarin(hans=km["zh-Hans"], hant=km["zh-Hant"]))

    if "kTotalStrokes" in char:
        kts = char["kTotalStrokes"]
        assert isinstance(kts, dict)
        c.kTotalStrokes.append(kTotalStrokes(hans=kts["zh-Hans"], hant=kts["zh-Hant"]))

    if "kHanyuPinyin" in char:
        for _khp in char["kHanyuPinyin"]:
            assert isinstance(_khp, dict)
            assert isinstance(_khp["locations"], list)
            assert isinstance(_khp["readings"], list)
            khp_readings: t.List[UnhnReading] = []
            khp_locations: t.List[UnhnLocation] = []

            for loc in _khp["locations"]:
                assert isinstance(loc, dict)
                khp_locations.append(
                    UnhnLocation(
                        volume=loc["volume"],
                        page=loc["page"],
                        character=loc["character"],
                        virtual=loc["virtual"],
                    )
                )
            for reading in _khp["readings"]:
                khp_readings.append(UnhnReading(reading=reading))
            c.kHanyuPinyin.append(
                kHanyuPinyin(
                    locations=khp_readings,
                    readings=khp_readings,
                )
            )

    if "kHanYu" in char:
        khy_locations: t.List[UnhnLocation] = []
        for _khy in char["kHanYu"]:
            assert isinstance(_khy, dict)
            khy_locations.append(
                UnhnLocation(
                    volume=_khy["volume"],
                    page=_khy["page"],
                    character=_khy["character"],
                    virtual=_khy["virtual"],
                )
            )
        c.kHanYu.append(kHanYu(locations=khy_locations))

    if "kIRGHanyuDaZidian" in char:
        _khdz_locations: t.List[UnhnLocation] = []
        for _khdz in char["kIRGHanyuDaZidian"]:
            assert isinstance(_khdz, dict)

            _khdz_locations.append(
                UnhnLocation(
                    volume=_khdz["volume"],
                    page=_khdz["page"],
                    character=_khdz["character"],
                    virtual=_khdz["virtual"],
                )
            )
        c.kIRGHanyuDaZidian.append(kIRGHanyuDaZidian(locations=_khdz_locations))

    if "kXHC1983" in char:
        for kxhc in char["kXHC1983"]:
            assert isinstance(kxhc, dict)
            assert isinstance(kxhc["locations"], list)
            kxhc_locations: t.List[UnhnLocationkXHC1983] = []
            for loc in kxhc["locations"]:
                kxhc_locations.append(
                    UnhnLocationkXHC1983(
                        page=loc["page"],
                        character=loc["character"],
                        entry=loc["entry"],
                        substituted=loc["substituted"],
                    )
                )
            c.kXHC1983.append(kXHC1983(readings=kxhc_locations))

    if "kCheungBauer" in char:
        for _kcb in char["kCheungBauer"]:
            assert isinstance(_kcb, dict)
            assert isinstance(_kcb["readings"], list)
            k_readings: t.List[UnhnReading] = []

            for reading in _kcb["readings"]:
                k_readings.append(UnhnReading(reading=reading))

            c.kCheungBauer.append(
                kCheungBauer(
                    radical=_kcb["radical"],
                    strokes=_kcb["strokes"],
                    cangjie=_kcb["cangjie"],
                    readings=k_readings,
                )
            )

    if "kRSAdobe_Japan1_6" in char:
        for _kaj in char["kRSAdobe_Japan1_6"]:
            assert isinstance(_kaj, dict)
            c.kRSAdobe_Japan1_6.append(
                kRSAdobe_Japan1_6(
                    type=_kaj["type"],
                    cid=_kaj["cid"],
                    radical=_kaj["radical"],
                    strokes=_kaj["strokes"],
                    strokes_residue=_kaj["strokes-residue"],
                )
            )

    if "kCihaiT" in char:
        for _kct in char["kCihaiT"]:
            assert isinstance(_kct, dict)
            c.kCihaiT.append(
                kCihaiT(page=_kct["page"], row=_kct["row"], character=_kct["character"])
            )

    if "kIICore" in char:
        for _kiic in char["kIICore"]:
            k_sources: t.List[kIICoreSource] = []
            assert isinstance(_kiic, dict)
            assert isinstance(_kiic["sources"], list)
            for _kiic_source in _kiic["sources"]:
                k_sources.append(kIICoreSource(source=_kiic_source))
            c.kIICore.append(kIICore(priority=_kiic["priority"], sources=k_sources))

    if "kDaeJaweon" in char:
        _kdj = char["kDaeJaweon"]
        assert isinstance(_kdj, dict)
        c.kDaeJaweon.append(
            kDaeJaweon(
                locations=[
                    UnhnLocation(
                        page=_kdj["page"],
                        character=_kdj["character"],
                        virtual=_kdj["virtual"],
                    )
                ]
            )
        )

    if "kIRGKangXi" in char:
        _kikx_locations: t.List[UnhnLocation] = []
        for _kikx in char["kIRGKangXi"]:
            assert isinstance(_kikx, dict)
            _kikx_locations.append(
                UnhnLocation(
                    page=_kikx["page"],
                    character=_kikx["character"],
                    virtual=_kikx["virtual"],
                )
            )
        c.kIRGKangXi.append(kIRGKangXi(locations=_kikx_locations))

    if "kIRGDaeJaweon" in char:
        _kidj_locations: t.List[UnhnLocation] = []
        for _kidj in char["kIRGDaeJaweon"]:
            assert isinstance(_kidj, dict)
            _kidj_locations.append(
                UnhnLocation(
                    page=_kidj["page"],
                    character=_kidj["character"],
                    virtual=_kidj["virtual"],
                )
            )
        c.kIRGDaeJaweon.append(kIRGDaeJaweon(locations=_kidj_locations))

    if "kFenn" in char:
        for _kf in char["kFenn"]:
            assert isinstance(_kf, dict)
            c.kFenn.append(kFenn(phonetic=_kf["phonetic"], frequency=_kf["frequency"]))

    if "kHanyuPinlu" in char:
        for _khp in char["kHanyuPinlu"]:
            assert isinstance(_khp, dict)
            assert isinstance(_khp["location"], dict)
            c.kHanyuPinlu.append(
                kHanyuPinlu(phonetic=_khp["phonetic"], frequency=_khp["frequency"])
            )

    if "kHDZRadBreak" in char:
        _khrb = char["kHDZRadBreak"]
        assert isinstance(_khrb, dict)
        assert isinstance(_khrb["location"], dict)
        c.kHDZRadBreak.append(
            kHDZRadBreak(
                radical=_khrb["radical"],
                ucn=_khrb["ucn"],
                locations=[
                    UnhnLocation(
                        volume=_khrb["location"]["volume"],
                        page=_khrb["location"]["page"],
                        character=_khrb["location"]["character"],
                        virtual=_khrb["location"]["virtual"],
                    )
                ],
            )
        )

    if "kSBGY" in char:
        _ksbgy_locations: t.List[UnhnLocation] = []
        for _ksbgy in char["kSBGY"]:
            assert isinstance(_ksbgy, dict)
            _ksbgy_locations.append(
                UnhnLocation(page=_ksbgy["page"], character=_ksbgy["character"])
            )
        c.kSBGY.append(kSBGY(locations=_ksbgy_locations))

    rs_fields = (  # radical-stroke fields, since they're the same structure
        ("kRSUnicode", kRSUnicode, c.kRSUnicode),
        ("kRSJapanese", kRSJapanese, c.kRSJapanese),
        ("kRSKangXi", kRSKangXi, c.kRSKangXi),
        ("kRSKanWa", kRSKanWa, c.kRSKanWa),
        ("kRSKorean", kRSKorean, c.kRSKorean),
    )

    for f_rs, RSModel, rs_column in rs_fields:
        if f_rs in char:
            for _md in char[f_rs]:
                assert isinstance(_md, dict)
                rs_column.append(
                    RSModel(
                        radical=_md["radical"],
                        strokes=_md["strokes"],
                        simplified=_md["simplified"],
                    )
                )

    irg_fields = (  # IRG, since they're the same structure
        ("kIRG_GSource", kIRG_GSource, c.kIRG_GSource),
        ("kIRG_HSource", kIRG_HSource, c.kIRG_HSource),
        ("kIRG_JSource", kIRG_JSource, c.kIRG_JSource),
        ("kIRG_KPSource", kIRG_KPSource, c.kIRG_KPSource),
        ("kIRG_KSource", kIRG_KSource, c.kIRG_KSource),
        ("kIRG_MSource", kIRG_MSource, c.kIRG_MSource),
        ("kIRG_TSource", kIRG_TSource, c.kIRG_TSource),
        ("kIRG_USource", kIRG_USource, c.kIRG_USource),
        ("kIRG_VSource", kIRG_VSource, c.kIRG_VSource),
    )

    for f_irg, IRGModel, column in irg_fields:
        if f_irg in char:
            _irg = char[f_irg]
            assert isinstance(_irg, dict)
            column.append(IRGModel(source=_irg["source"], location=_irg["location"]))

    if "kGSR" in char:
        for _kgsr in char["kGSR"]:
            assert isinstance(_kgsr, dict)
            c.kGSR.append(
                kGSR(
                    set=_kgsr["set"],
                    letter=_kgsr["letter"],
                    apostrophe=_kgsr["apostrophe"],
                )
            )

    if "kCheungBauerIndex" in char:
        kcbi = char["kCheungBauerIndex"]
        assert isinstance(kcbi, dict)
        assert isinstance(kcbi["location"], dict)
        c.kCheungBauerIndex.append(
            kCheungBauerIndex(
                locations=[
                    UnhnLocation(
                        page=kcbi["location"]["page"],
                        character=kcbi["location"]["character"],
                    )
                ]
            )
        )

    if "kFennIndex" in char:
        _kFennIndex = char["kFennIndex"]
        assert isinstance(_kFennIndex, dict)
        assert isinstance(_kFennIndex["location"], dict)
        c.kFennIndex.append(
            kFennIndex(
                locations=UnhnLocation(
                    page=_kFennIndex["location"]["page"],
                    character=_kFennIndex["location"]["character"],
                )
            )
        )
