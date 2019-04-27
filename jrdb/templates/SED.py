import logging

import numpy as np
import pandas as pd
from django.db import IntegrityError, transaction

from ..models import Jockey, Trainer, Race, Contender, Horse, choices
from .template import Template, startswith
from .item import (
    StringItem,
    ForeignKeyItem,
    IntegerItem,
    ChoiceItem,
    FloatItem,
    InvokeItem,
    parse_int_or,
    parse_float_or
)

logger = logging.getLogger(__name__)


def purse(se: pd.Series):
    return (se.str.strip()
            .where(lambda x: x != '', 0)
            .astype(float)
            .rename('contender__purse'))


def weight_diff(se: pd.Series):
    return (se.str.replace(' ', '')
            .apply(parse_int_or, args=(np.nan,))
            .astype('Int64')
            .rename('contender__weight_diff'))


def c1p(se: pd.Series):
    return (se.apply(parse_float_or, args=(np.nan,))
            .where(lambda x: x != 0)
            .astype('Int64')
            .rename('contender__c1p'))


def c2p(se: pd.Series):
    return (se.apply(parse_float_or, args=(np.nan,))
            .where(lambda x: x != 0)
            .astype('Int64')
            .rename('contender__c2p'))


def c3p(se: pd.Series):
    return (se.apply(parse_float_or, args=(np.nan,))
            .where(lambda x: x != 0)
            .astype('Int64')
            .rename('contender__c3p'))


def c4p(se: pd.Series):
    return (se.apply(parse_float_or, args=(np.nan,))
            .where(lambda x: x != 0)
            .astype('Int64')
            .rename('contender__c4p'))


class SED(Template):
    """
    http://www.jrdb.com/program/Sed/sed_doc.txt

    The "種別" values in the above document are incorrect.
    The correct values can be found [here](http://www.jrdb.com/program/jrdb_code.txt)
    """
    name = 'JRDB成績データ（SED）'

    items = [
        # レースキー
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('馬番', 2, 8, 'jrdb.Contender.num'),
        StringItem('血統登録番号', 8, 10, 'jrdb.Horse.pedigree_reg_num'),
        # StringItem('race_date', '年月日', '8',  '19', 'YYYYMMDD <-暫定版より順序'),  # IGNORED (use value from BA),
        StringItem('馬名', 36, 26, 'jrdb.Horse.name'),

        # レース条件
        IntegerItem('距離', 4, 62, 'jrdb.Race.distance'),
        ChoiceItem('芝ダ障害コード', 1, 66, 'jrdb.Race.surface', choices.SURFACE.options()),
        ChoiceItem('右左', 1, 67, 'jrdb.Race.direction', choices.DIRECTION.options()),
        ChoiceItem('内外', 1, 68, 'jrdb.Race.course_inout', choices.COURSE_INOUT.options()),
        ChoiceItem('馬場状態', 2, 69, 'jrdb.Race.track_cond', choices.TRACK_CONDITION.options()),
        ChoiceItem('種別', 2, 71, 'jrdb.Race.category', choices.RACE_CATEGORY.options()),
        ForeignKeyItem('条件', 2, 73, 'jrdb.Race.cond', 'jrdb.RaceConditionCode.key'),
        ChoiceItem('馬の種類による条件', 1, 75, 'jrdb.Race.horse_type_symbol', choices.RACE_HORSE_TYPE_SYMBOL.options()),
        ChoiceItem('馬の性別による条件', 1, 76, 'jrdb.Race.horse_sex_symbol', choices.RACE_HORSE_SEX_SYMBOL.options()),
        ChoiceItem('交流競走の指定', 1, 77, 'jrdb.Race.interleague_symbol', choices.RACE_INTERLEAGUE_SYMBOL.options()),

        ChoiceItem('重量', 1, 78, 'jrdb.Race.impost_class', choices.IMPOST_CLASS.options()),
        ChoiceItem('グレード', 1, 79, 'jrdb.Race.grade', choices.GRADE.options()),
        StringItem('レース名', 50, 80, 'jrdb.Race.name'),
        IntegerItem('頭数', 2, 130, 'jrdb.Race.contender_count'),
        StringItem('レース名略称', 8, 132, 'jrdb.Race.name_abbr'),
        # 馬成績
        IntegerItem('着順', 2, 140, 'jrdb.Contender.order_of_finish'),
        ChoiceItem('異常区分', 1, 142, 'jrdb.Contender.penalty', choices.PENALTY.options()),
        FloatItem('タイム', 4, 143, 'jrdb.Contender.time', np.nan, 0.1),
        FloatItem('斤量', 3, 147, 'jrdb.Contender.mounted_weight', scale=0.1),
        StringItem('騎手名', 12, 150, 'jrdb.Jockey.name'),
        StringItem('調教師名', 12, 162, 'jrdb.Trainer.name'),
        FloatItem('確定単勝オッズ', 6, 174, 'jrdb.Contender.odds_win', np.nan),
        IntegerItem('確定単勝人気順位', 2, 180, 'jrdb.Contender.popularity'),
        # ＪＲＤＢデータ
        IntegerItem('ＩＤＭ', 3, 182, 'jrdb.Contender.IDM'),
        IntegerItem('素点', 3, 185, 'jrdb.Contender.speed_idx'),
        IntegerItem('馬場差', 3, 188, 'jrdb.Race.track_speed_shift'),
        IntegerItem('ペース', 3, 191, 'jrdb.Contender.pace'),
        IntegerItem('出遅', 3, 194, 'jrdb.Contender.late_start'),
        IntegerItem('位置取', 3, 197, 'jrdb.Contender.positioning'),
        IntegerItem('不利', 3, 200, 'jrdb.Contender.disadvt'),
        IntegerItem('前不利', 3, 203, 'jrdb.Contender.b3f_disadvt'),
        IntegerItem('中不利', 3, 206, 'jrdb.Contender.mid_disadvt'),
        IntegerItem('後不利', 3, 209, 'jrdb.Contender.f3f_disadvt'),
        # StringItem('レース', 3, 212, 'race_ind'),  # IGNORED (単位/意味不明)
        ChoiceItem('コース取り', 1, 215, 'jrdb.Contender.race_line', choices.RACE_LINE.options()),
        ChoiceItem('上昇度コード', 1, 216, 'jrdb.Contender.improvement', choices.IMPROVEMENT.options()),
        # TODO: Why does race_class_code differ between horses in the same race?
        # StringItem('クラスコード', 2, 217, 'race_class_code'),  # IGNORED
        ChoiceItem('馬体コード', 1, 219, 'jrdb.Contender.physique', choices.PHYSIQUE.options()),
        ChoiceItem('気配コード', 1, 220, 'jrdb.Contender.demeanor', choices.DEMEANOR.options()),
        ChoiceItem('レースペース', 1, 221, 'jrdb.Race.pace_cat', choices.PACE_CATEGORY.options()),
        ChoiceItem('馬ペース', 1, 222, 'jrdb.Contender.pace_cat', choices.PACE_CATEGORY.options()),
        # テン指数はダッシュ力を意味する（元になる数値は前３Ｆタイム）
        FloatItem('テン指数', 5, 223, 'jrdb.Contender.b3f_time_idx', np.nan),
        # 勝負所からの最後の脚（元になる数値は後3Fタイム）
        FloatItem('上がり指数', 5, 228, 'jrdb.Contender.f3f_time_idx', np.nan),
        # ペース指数は道中どれぐらいのペースで後３Ｆを走ったか（元になる数値は走破タイム-後3Fタイム）
        FloatItem('ペース指数', 5, 233, 'jrdb.Contender.pace_idx', np.nan),
        FloatItem('レースＰ指数', 5, 238, 'jrdb.Race.pace_idx', np.nan),
        # for 1st place horses, the second place horse name/time
        # for 2nd > place horses, the first place horse name/time
        # StringItem('1(2)着馬名', 12, 243, 'fos_horse_name'),  # IGNORED
        FloatItem('1(2)着タイム差', 3, 255, 'jrdb.Contender.margin', np.nan, 0.1),
        FloatItem('前３Ｆタイム', 3, 258, 'jrdb.Contender.b3f_time', np.nan, 0.1),
        FloatItem('後３Ｆタイム', 3, 261, 'jrdb.Contender.f3f_time', np.nan, 0.1),
        # StringItem('備考', 24, 264, 'note'),  # IGNORED
        FloatItem('確定複勝オッズ下', 6, 290, 'jrdb.Contender.odds_show', np.nan),
        FloatItem('10時単勝オッズ', 6, 296, 'jrdb.Contender.odds_win_10AM', np.nan),
        FloatItem('10時複勝オッズ', 6, 302, 'jrdb.Contender.odds_show_10AM', np.nan),
        InvokeItem('コーナー順位１', 2, 308, c1p),
        InvokeItem('コーナー順位２', 2, 310, c2p),
        InvokeItem('コーナー順位３', 2, 312, c3p),
        InvokeItem('コーナー順位４', 2, 314, c4p),
        FloatItem('前３Ｆ先頭差', 3, 316, 'jrdb.Contender.b3f_1p_margin', np.nan, 0.1),
        FloatItem('後３Ｆ先頭差', 3, 319, 'jrdb.Contender.f3f_1p_margin', np.nan, 0.1),
        StringItem('騎手コード', 5, 322, 'jrdb.Jockey.code'),
        StringItem('調教師コード', 5, 327, 'jrdb.Trainer.code'),
        IntegerItem('馬体重', 3, 332, 'jrdb.Contender.weight'),
        InvokeItem('馬体重増減', 3, 335, weight_diff),
        ChoiceItem('天候コード', 1, 338, 'jrdb.Race.weather', choices.WEATHER.options()),
        ChoiceItem('コース', 1, 339, 'jrdb.Race.course_label', choices.COURSE_LABEL.options()),
        ChoiceItem('レース脚質', 1, 340, 'jrdb.Contender.run_style', choices.RUNNING_STYLE.options()),
        # StringItem('単勝', 7, 341, 'win_payoff_yen'),  # IGNORED
        # StringItem('複勝', 7, 348, 'show_payoff_yen'),  # IGNORED
        InvokeItem('本賞金', 5, 355, purse),
        # StringItem('収得賞金', 5, 360, 'p1_prize'),  # IGNORED
        ForeignKeyItem('レースペース流れ', 2, 365, 'jrdb.Race.pace_flow', 'jrdb.PaceFlowCode.key'),
        ForeignKeyItem('馬ペース流れ', 2, 367, 'jrdb.Contender.pace_flow', 'jrdb.PaceFlowCode.key'),
        ChoiceItem('４角コース取り', 1, 369, 'jrdb.Contender.c4_race_line', choices.RACE_LINE.options()),
    ]

    @transaction.atomic
    def persist(self):
        for _, row in self.clean().iterrows():
            r = row.pipe(startswith, 'race__', rename=True).dropna().to_dict()
            race, _ = Race.objects.get_or_create(racetrack_id=r.pop('racetrack_id'), yr=r.pop('yr'),
                                                 round=r.pop('round'), day=r.pop('day'), num=r.pop('num'))

            h = row.pipe(startswith, 'horse__', rename=True).dropna().to_dict()
            horse, _ = Horse.objects.get_or_create(pedigree_reg_num=h.pop('pedigree_reg_num'), defaults=h)

            j = row.pipe(startswith, 'jockey__', rename=True).dropna().to_dict()
            jockey, _ = Jockey.objects.get_or_create(code=j.pop('code'), defaults=j)

            t = row.pipe(startswith, 'trainer__', rename=True).dropna().to_dict()
            trainer, _ = Trainer.objects.get_or_create(code=t.pop('code'), defaults=t)

            try:
                c = row.pipe(startswith, 'contender__', rename=True).dropna().to_dict()
                c['horse_id'] = horse.id
                c['jockey_id'] = jockey.id
                c['trainer_id'] = trainer.id
                Contender.objects.update_or_create(race=race, num=c.pop('num'), defaults=c)
            except IntegrityError as e:
                logger.exception(e)
