# flake8: noqa: PERF401
"""Import functionality for UNIHAN DB."""

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
    kRSUnicode,
    kSBGY,
    kTotalStrokes,
    kXHC1983,
)
from unihan_etl.expansion import kRSSimplifiedType


def import_char(
    c: Unhn,
    char: dict[
        str,
        t.Union[
            dict[
                str,
                t.Union[int, str, list[dict[str, object]], dict[str, object]],
            ],
            list[dict[str, object]],
            dict[str, object],
        ],
    ],
) -> None:
    """Import character data into Unhn model (row in Unhn table)."""
    if "kDefinition" in char:
        for kd in char["kDefinition"]:
            c.kDefinition.append(kDefinition(definition=kd))
    if "kCantonese" in char:
        for kc in char["kCantonese"]:
            c.kCantonese.append(kCantonese(definition=kc))
    if "kCCCII" in char:
        for kci in char["kCCCII"]:
            assert isinstance(kci, str)
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
            khp_readings: list[UnhnReading] = []
            khp_locations: list[UnhnLocation] = []

            for loc in _khp["locations"]:
                assert isinstance(loc, dict)
                khp_locations.append(
                    UnhnLocation(
                        volume=loc["volume"],
                        page=loc["page"],
                        character=loc["character"],
                        virtual=loc["virtual"],
                    ),
                )
            for reading in _khp["readings"]:
                khp_readings.append(UnhnReading(reading=reading))
            c.kHanyuPinyin.append(
                kHanyuPinyin(
                    locations=khp_locations,
                    readings=khp_readings,
                ),
            )

    if "kHanYu" in char:
        khy_locations: list[UnhnLocation] = []
        for _khy in char["kHanYu"]:
            assert isinstance(_khy, dict)
            khy_locations.append(
                UnhnLocation(
                    volume=_khy["volume"],
                    page=_khy["page"],
                    character=_khy["character"],
                    virtual=_khy["virtual"],
                ),
            )
        c.kHanYu.append(kHanYu(locations=khy_locations))

    if "kIRGHanyuDaZidian" in char:
        khdz_locations: list[UnhnLocation] = []
        for _khdz in char["kIRGHanyuDaZidian"]:
            assert isinstance(_khdz, dict)

            khdz_locations.append(
                UnhnLocation(
                    volume=_khdz["volume"],
                    page=_khdz["page"],
                    character=_khdz["character"],
                    virtual=_khdz["virtual"],
                ),
            )
        c.kIRGHanyuDaZidian.append(kIRGHanyuDaZidian(locations=khdz_locations))

    if "kXHC1983" in char:
        for kxhc in char["kXHC1983"]:
            assert isinstance(kxhc, dict)
            assert isinstance(kxhc["locations"], list)
            kxhc_locations: list[UnhnLocationkXHC1983] = []
            for loc in kxhc["locations"]:
                kxhc_locations.append(
                    UnhnLocationkXHC1983(
                        page=loc["page"],
                        character=loc["character"],
                        entry=loc["entry"],
                        substituted=loc["substituted"],
                    ),
                )
            c.kXHC1983.append(kXHC1983(locations=kxhc_locations))

    if "kCheungBauer" in char:
        for _kcb in char["kCheungBauer"]:
            assert isinstance(_kcb, dict)
            assert isinstance(_kcb["readings"], list)
            k_readings: list[UnhnReading] = []

            for reading in _kcb["readings"]:
                k_readings.append(UnhnReading(reading=reading))

            c.kCheungBauer.append(
                kCheungBauer(
                    radical=_kcb["radical"],
                    strokes=_kcb["strokes"],
                    cangjie=_kcb["cangjie"],
                    readings=k_readings,
                ),
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
                ),
            )

    if "kCihaiT" in char:
        for _kct in char["kCihaiT"]:
            assert isinstance(_kct, dict)
            c.kCihaiT.append(
                kCihaiT(
                    page=_kct["page"],
                    row=_kct["row"],
                    character=_kct["character"],
                ),
            )

    if "kIICore" in char:
        for _kiic in char["kIICore"]:
            k_sources: list[kIICoreSource] = []
            assert isinstance(_kiic, dict)
            assert isinstance(_kiic["sources"], list)
            for _kiic_source in _kiic["sources"]:
                k_sources.append(kIICoreSource(source=_kiic_source))
            c.kIICore.append(kIICore(priority=_kiic["priority"], sources=k_sources))

    if "kDaeJaweon" in char:
        kdj = char["kDaeJaweon"]
        assert isinstance(kdj, dict)
        c.kDaeJaweon.append(
            kDaeJaweon(
                locations=[
                    UnhnLocation(
                        page=kdj["page"],
                        character=kdj["character"],
                        virtual=kdj["virtual"],
                    ),
                ],
            ),
        )

    if "kIRGKangXi" in char:
        kikx_locations: list[UnhnLocation] = []
        for _kikx in char["kIRGKangXi"]:
            assert isinstance(_kikx, dict)
            kikx_locations.append(
                UnhnLocation(
                    page=_kikx["page"],
                    character=_kikx["character"],
                    virtual=_kikx["virtual"],
                ),
            )
        c.kIRGKangXi.append(kIRGKangXi(locations=kikx_locations))

    if "kIRGDaeJaweon" in char:
        kidj_locations: list[UnhnLocation] = []
        for _kidj in char["kIRGDaeJaweon"]:
            assert isinstance(_kidj, dict)
            kidj_locations.append(
                UnhnLocation(
                    page=_kidj["page"],
                    character=_kidj["character"],
                    virtual=_kidj["virtual"],
                ),
            )
        c.kIRGDaeJaweon.append(kIRGDaeJaweon(locations=kidj_locations))

    if "kFenn" in char:
        for _kf in char["kFenn"]:
            assert isinstance(_kf, dict)
            c.kFenn.append(kFenn(phonetic=_kf["phonetic"], frequency=_kf["frequency"]))

    if "kHanyuPinlu" in char:
        for _khp in char["kHanyuPinlu"]:
            assert isinstance(_khp, dict)
            c.kHanyuPinlu.append(
                kHanyuPinlu(phonetic=_khp["phonetic"], frequency=_khp["frequency"]),
            )

    if "kHDZRadBreak" in char:
        khrb = char["kHDZRadBreak"]
        assert isinstance(khrb, dict)
        assert isinstance(khrb["location"], dict)
        c.kHDZRadBreak.append(
            kHDZRadBreak(
                radical=khrb["radical"],
                ucn=khrb["ucn"],
                locations=[
                    UnhnLocation(
                        volume=khrb["location"]["volume"],
                        page=khrb["location"]["page"],
                        character=khrb["location"]["character"],
                        virtual=khrb["location"]["virtual"],
                    ),
                ],
            ),
        )

    if "kSBGY" in char:
        ksbgy_locations: list[UnhnLocation] = []
        for _ksbgy in char["kSBGY"]:
            assert isinstance(_ksbgy, dict)
            ksbgy_locations.append(
                UnhnLocation(page=_ksbgy["page"], character=_ksbgy["character"]),
            )
        c.kSBGY.append(kSBGY(locations=ksbgy_locations))

    rs_fields = (  # radical-stroke fields, since they're the same structure
        ("kRSUnicode", kRSUnicode, c.kRSUnicode),
    )

    for f_rs, RSModel, rs_column in rs_fields:
        if f_rs in char:
            for _md in char[f_rs]:
                assert isinstance(_md, dict)
                rs_column.append(
                    RSModel(
                        radical=_md["radical"],
                        strokes=_md["strokes"],
                        simplified=_md["simplified"].value
                        if isinstance(_md["simplified"], kRSSimplifiedType)
                        else "",
                    ),
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
            irg = char[f_irg]
            assert isinstance(irg, dict)
            column.append(IRGModel(source=irg["source"], location=irg["location"]))

    if "kGSR" in char:
        for _kgsr in char["kGSR"]:
            assert isinstance(_kgsr, dict)
            c.kGSR.append(
                kGSR(
                    set=_kgsr["set"],
                    letter=_kgsr["letter"],
                    apostrophe=_kgsr["apostrophe"],
                ),
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
                    ),
                ],
            ),
        )

    if "kFennIndex" in char:
        kFennIndex_ = char["kFennIndex"]
        assert isinstance(kFennIndex_, dict)
        assert isinstance(kFennIndex_["location"], dict)
        c.kFennIndex.append(
            kFennIndex(
                locations=UnhnLocation(
                    page=kFennIndex_["location"]["page"],
                    character=kFennIndex_["location"]["character"],
                ),
            ),
        )
