from .template import Template, startswith
from .item import ForeignKeyItem, IntegerItem, StringItem, BooleanItem, ArrayItem


class SKB(Template):
    """
    http://www.jrdb.com/program/Skb/skb_doc.txt
    """
    name = 'JRDB成績拡張データ（SKB）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('馬番', 2, 8, 'jrdb.Contender.num'),
        StringItem('血統登録番号', 8, 10, 'jrdb.Horse.pedigree_reg_num'),
        # ['race_date', '年月日', '8', '9', '19', 'YYYYMMDD'],  # IGNORED (use value from BAC)
        ArrayItem('特記コード', 3 * 6, 26, 'jrdb.Contender.sp_mention', 6),
        ArrayItem('馬具コード', 3 * 8, 44, 'jrdb.Contender.horse_gear', 8),
        ArrayItem('総合', 3 * 3, 68, 'jrdb.Contender.hoof_overall', 3),
        ArrayItem('左前', 3 * 3, 77, 'jrdb.Contender.hoof_front_left', 3),
        ArrayItem('右前', 3 * 3, 86, 'jrdb.Contender.hoof_front_right', 3),
        ArrayItem('左後', 3 * 3, 95, 'jrdb.Contender.hoof_back_left', 3),
        ArrayItem('右後', 3 * 3, 104, 'jrdb.Contender.hoof_back_right', 3),
        StringItem('パドックコメント', 40, 113, 'jrdb.Contender.paddock_comment'),
        StringItem('脚元コメント', 40, 153, 'jrdb.Contender.hoof_comment'),
        StringItem('馬具', 40, 193, 'jrdb.Contender.horse_gear_or_other_comment'),
        StringItem('レースコメント', 40, 233, 'jrdb.Contender.race_comment'),
        ForeignKeyItem('ハミ', 3, 273, 'jrdb.Contender.bit', 'jrdb.HorseGearCode.key'),
        BooleanItem('バンテージ', 3, 276, 'jrdb.Contender.bandage', value_true='007', value_false=''),
        ForeignKeyItem('蹄鉄', 3, 279, 'jrdb.Contender.horseshoe', 'jrdb.HorseGearCode.key'),
        ForeignKeyItem('蹄状態', 3, 282, 'jrdb.Contender.hoof_cond', 'jrdb.HorseGearCode.key'),
        ForeignKeyItem('ソエ', 3, 285, 'jrdb.Contender.periostitis', 'jrdb.HorseGearCode.key'),
        ForeignKeyItem('骨瘤', 3, 288, 'jrdb.Contender.exostosis', 'jrdb.HorseGearCode.key'),
    ]

    def load(self):
        pdf = self.transform.pipe(startswith, 'program__', rename=True)
        programs = self.loader_cls(pdf, 'jrdb.Program').load()

        hdf = self.transform.pipe(startswith, 'horse__', rename=True)
        horses = self.loader_cls(hdf, 'jrdb.Horse').load()

        rdf = self.transform.pipe(startswith, 'race__', rename=True)
        rdf['program_id'] = pdf.merge(programs, how='left').id
        races = self.loader_cls(rdf, 'jrdb.Race').load()

        cdf = self.transform.pipe(startswith, 'contender__', rename=True)
        cdf['race_id'] = rdf[['program_id', 'num']].merge(races, how='left').id
        cdf['horse_id'] = hdf.merge(horses, how='left').id
        self.loader_cls(cdf, 'jrdb.Contender').load()
