import numpy as np

from ..helpers import startswith
from ..models import choices
from .template import Template
from .item import ForeignKeyItem, IntegerItem, StringItem, ChoiceItem, BooleanItem, FloatItem


class KAB(Template):
    """
    http://www.jrdb.com/program/Kab/kab_doc.txt

    010821200809133土札幌11 222-2 -10 0 0 0 1 111-7 49 214  000
    060841200809131土中山11 111-12-3-2-10 0 1 111-1241 110  007.5

    TODO: Keep IGNORE columns; but add way to filter out before load
    """
    name = 'JRDB開催データ（KAB）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        # ['date', '年月日', None, '8', '9', '7', 'YYYYMMDD'], # IGNORED (supplied in BAC)
        ChoiceItem('開催区分', 1, 14, 'jrdb.Program.host_category', choices.HOST_CATEGORY.options()),
        # ['weekday', '曜日', None, '2', 'X', '16', '日－土'],  # IGNORED (inferrable)
        # ['racename', '場名', None, '4', 'X', '18', '競馬場名'],  # IGNORED (inferrable)
        ChoiceItem('天候コード', 1, 21, 'jrdb.Program.weather', choices.WEATHER.options()),
        ChoiceItem('芝馬場状態コード', 2, 22, 'jrdb.Program.turf_cond', choices.TRACK_CONDITION_KA.options()),
        ChoiceItem('芝馬場状態内', 1, 24, 'jrdb.Program.turf_cond_inner', choices.TRACK_CONDITION_KA.options()),
        ChoiceItem('芝馬場状態中', 1, 25, 'jrdb.Program.turf_cond_mid', choices.TRACK_CONDITION_KA.options()),
        ChoiceItem('芝馬場状態外', 1, 26, 'jrdb.Program.turf_cond_outer', choices.TRACK_CONDITION_KA.options()),
        IntegerItem('芝馬場差', 3, 27, 'jrdb.Program.turf_speed_shift'),
        IntegerItem('直線馬場差最内', 2, 30, 'jrdb.Program.hs_speed_shift_innermost'),
        IntegerItem('直線馬場差内', 2, 32, 'jrdb.Program.hs_speed_shift_inner'),
        IntegerItem('直線馬場差中', 2, 34, 'jrdb.Program.hs_speed_shift_mid'),
        IntegerItem('直線馬場差外', 2, 36, 'jrdb.Program.hs_speed_shift_outer'),
        IntegerItem('直線馬場差大外', 2, 38, 'jrdb.Program.hs_speed_shift_outermost'),
        ChoiceItem('ダ馬場状態コード', 2, 40, 'jrdb.Program.dirt_cond', choices.TRACK_CONDITION_KA.options()),
        ChoiceItem('ダ馬場状態内', 1, 42, 'jrdb.Program.dirt_cond_inner', choices.TRACK_CONDITION_KA.options()),
        ChoiceItem('ダ馬場状態中', 1, 43, 'jrdb.Program.dirt_cond_mid', choices.TRACK_CONDITION_KA.options()),
        ChoiceItem('ダ馬場状態外', 1, 44, 'jrdb.Program.dirt_cond_outer', choices.TRACK_CONDITION_KA.options()),
        IntegerItem('ダ馬場差', 3, 45, 'jrdb.Program.dirt_speed_shift'),
        # StringItem('データ区分', 1, 48, 'jrdb.Program.data_category_1'), # IGNORED (not needed)
        IntegerItem('連続何日目', 2, 49, 'jrdb.Program.nth_occurrence'),
        ChoiceItem('芝種類', 1, 51, 'jrdb.Program.turf_type', choices.TURF_TYPE.options()),
        FloatItem('草丈', 4, 52, 'jrdb.Program.grass_height', default=np.nan),
        BooleanItem('転圧', 1, 56, 'jrdb.Program.used_rolling_compactor'),
        BooleanItem('凍結防止剤', 1, 57, 'jrdb.Program.used_anti_freeze_agent'),
        FloatItem('中間降水量', 5, 58, 'jrdb.Program.mm_precipitation', default=np.nan),
    ]

    def load(self):
        df = self.transform.pipe(startswith, 'program__', rename=True)
        self.loader_cls(df, 'jrdb.Program').load()
