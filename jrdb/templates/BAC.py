import pandas as pd

from ..models import choices
from .item import DateTimeItem, ChoiceItem, ForeignKeyItem, IntegerItem, StringItem, InvokeItem, BooleanItem
from .loader import ProgramRaceLoadMixin
from .template import Template


def nth_occurrence(se: pd.Series):
    # casting to float prior to Int64 is necessary
    # to convert strings to numbers
    return (se.str.extract(r'([0-9]+)', expand=False)
            .astype(float)
            .astype('Int64')
            .rename('race__nth_occurrence'))


class BAC(Template, ProgramRaceLoadMixin):
    """
    レース番組情報

    http://www.jrdb.com/program/Bac/bac_doc.txt
    """
    name = 'JRDB番組データ（BAC）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        DateTimeItem('年月日/発走時間', 12, 8, 'jrdb.Race.started_at'),
        IntegerItem('距離', 4, 20, 'jrdb.Race.distance'),
        ChoiceItem('芝ダ障害コード', 1, 24, 'jrdb.Race.surface', choices.SURFACE.options()),
        ChoiceItem('右左', 1, 25, 'jrdb.Race.direction', choices.DIRECTION.options()),
        ChoiceItem('内外', 1, 26, 'jrdb.Race.course_inout', choices.COURSE_INOUT.options()),
        ChoiceItem('種別', 2, 27, 'jrdb.Race.category', choices.RACE_CATEGORY.options()),
        ForeignKeyItem('条件', 2, 29, 'jrdb.Race.cond', 'jrdb.RaceConditionCode.key'),
        ChoiceItem('馬の種類による条件', 1, 31, 'jrdb.Race.horse_type_symbol', choices.RACE_HORSE_TYPE_SYMBOL.options()),
        ChoiceItem('馬の性別による条件', 1, 32, 'jrdb.Race.horse_sex_symbol', choices.RACE_HORSE_SEX_SYMBOL.options()),
        ChoiceItem('交流競走の指定', 1, 33, 'jrdb.Race.interleague_symbol', choices.RACE_INTERLEAGUE_SYMBOL.options()),
        ChoiceItem('重量', 1, 34, 'jrdb.Race.impost_class', choices.IMPOST_CLASS.options()),
        ChoiceItem('グレード', 1, 35, 'jrdb.Race.grade', choices.GRADE.options()),
        StringItem('レース名', 50, 36, 'jrdb.Race.name'),
        InvokeItem('回数', 8, 86, nth_occurrence),
        IntegerItem('頭数', 2, 94, 'jrdb.Race.contender_count'),
        ChoiceItem('コース', 1, 96, 'jrdb.Race.course_label', choices.COURSE_LABEL.options()),
        ChoiceItem('開催区分', 1, 97, 'jrdb.Race.host_category', choices.HOST_CATEGORY.options()),
        StringItem('レース名短縮', 8, 98, 'jrdb.Race.name_abbr'),
        StringItem('レース名９文字', 18, 106, 'jrdb.Race.name_short'),
        # Item('data_category', 'データ区分', 1, 124),
        IntegerItem('１着賞金', 5, 125, 'jrdb.Race.p1_purse'),
        IntegerItem('２着賞金', 5, 130, 'jrdb.Race.p2_purse'),
        IntegerItem('３着賞金', 5, 135, 'jrdb.Race.p3_purse'),
        IntegerItem('４着賞金', 5, 140, 'jrdb.Race.p4_purse'),
        IntegerItem('５着賞金', 5, 145, 'jrdb.Race.p5_purse'),
        IntegerItem('１着算入賞金', 5, 150, 'jrdb.Race.p1_prize'),
        IntegerItem('２着算入賞金', 5, 155, 'jrdb.Race.p2_prize'),
        BooleanItem('単勝', 1, 160, 'jrdb.Race.sold_win'),
        BooleanItem('複勝', 1, 161, 'jrdb.Race.sold_show'),
        BooleanItem('枠連', 1, 162, 'jrdb.Race.sold_bracket_quinella'),
        BooleanItem('馬連', 1, 163, 'jrdb.Race.sold_quinella'),
        BooleanItem('馬単', 1, 164, 'jrdb.Race.sold_exacta'),
        BooleanItem('ワイド', 1, 165, 'jrdb.Race.sold_duet'),
        BooleanItem('３連複', 1, 166, 'jrdb.Race.sold_trio'),
        BooleanItem('３連単', 1, 167, 'jrdb.Race.sold_trifecta'),
        IntegerItem('WIN5フラグ', 1, 176, 'jrdb.Race.win5'),
    ]
