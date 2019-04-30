import logging

from ..models import Horse, Race, Program
from .template import Template, startswith, PostgresUpsertMixin
from .item import ForeignKeyItem, IntegerItem, StringItem, BooleanItem

logger = logging.getLogger(__name__)


class SKB(Template, PostgresUpsertMixin):
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
        ForeignKeyItem('特記コード', 3, 26, 'jrdb.Contender.sp_mention', 'jrdb.SpecialMentionCode.key'),
        ForeignKeyItem('馬具コード', 3, 44, 'jrdb.Contender.horse_gear', 'jrdb.HorseGearCode.key'),
        ForeignKeyItem('総合', 3, 68, 'jrdb.Contender.hoof_overall', 'jrdb.HorseGearCode.key'),
        ForeignKeyItem('左前', 3, 77, 'jrdb.Contender.hoof_front_left', 'jrdb.HorseGearCode.key'),
        ForeignKeyItem('右前', 3, 86, 'jrdb.Contender.hoof_front_right', 'jrdb.HorseGearCode.key'),
        ForeignKeyItem('左後', 3, 95, 'jrdb.Contender.hoof_back_left', 'jrdb.HorseGearCode.key'),
        ForeignKeyItem('右後', 3, 104, 'jrdb.Contender.hoof_back_right', 'jrdb.HorseGearCode.key'),
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

    def persist(self):
        self.upsert('jrdb.Program')
        pdf = self.clean.pipe(startswith, 'program__', rename=True)
        programs = (Program.objects
                    .filter(racetrack_id__in=pdf.racetrack_id, yr__in=pdf.yr, round__in=pdf['round'], day__in=pdf.day)
                    .values('id', 'racetrack_id', 'yr', 'round', 'day').to_dataframe())
        program_id = pdf.merge(programs, how='left').id

        self.upsert('jrdb.Race', program_id=program_id)
        rdf = self.clean.pipe(startswith, 'race__', rename=True)
        races = (Race.objects.filter(program_id__in=program_id, num__in=rdf.num).values('id', 'program_id', 'num')
                 .to_dataframe())

        hdf = self.clean.pipe(startswith, 'horse__', rename=True)
        self.upsert('jrdb.Horse')
        horses = (Horse.objects.filter(pedigree_reg_num__in=hdf.pedigree_reg_num).values('id', 'pedigree_reg_num')
                  .to_dataframe())

        rdf['program_id'] = program_id
        race_id = rdf[['program_id', 'num']].merge(races, how='left').id
        horse_id = hdf.merge(horses, how='left').id

        self.upsert('jrdb.Contender', race_id=race_id, horse_id=horse_id)
