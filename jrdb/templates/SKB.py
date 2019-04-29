import logging

import pandas as pd
from django.db import transaction, IntegrityError, connection

from ..models import Horse, Race, Contender, Program
from .template import Template, startswith
from .item import ForeignKeyItem, IntegerItem, StringItem, BooleanItem

logger = logging.getLogger(__name__)


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

    def persist_races(self):
        sep = ','

        p_df = self.clean.pipe(startswith, 'program__', rename=True)
        r_df = self.clean.pipe(startswith, 'race__', rename=True)

        # PROGRAM
        p_cols = sep.join('"{}"'.format(key) for key in p_df.columns)
        p_vals = sep.join(map(str, map(tuple, p_df.values))).replace('nan', 'NULL')

        with connection.cursor() as c:
            c.execute(
                f'INSERT INTO programs ({p_cols}) '
                f'VALUES {p_vals} '
                f'ON CONFLICT DO NOTHING'
            )

        # RACE
        p_lookup = {
            'day__in': p_df.day,
            'racetrack_id__in': p_df.racetrack_id,
            'yr__in': p_df.yr,
            'round__in': p_df['round']
        }

        p_search = Program.objects.filter(**p_lookup).values('id', 'racetrack_id', 'yr', 'round', 'day')
        p_search_df = pd.DataFrame(p_search)

        r_df['program_id'] = p_df.merge(p_search_df).id

        r_cols = sep.join('"{}"'.format(key) for key in r_df.columns)
        r_vals = sep.join(map(str, map(tuple, r_df.values))).replace('nan', 'NULL')

        r_uniq = ['program_id', 'num']
        r_uniq_str = sep.join('"{}"'.format(key) for key in r_uniq)
        r_updates = sep.join((f'{key}=excluded.{key}' for key in r_df.columns if key not in r_uniq))

        with connection.cursor() as c:
            c.execute(
                f'INSERT INTO races ({r_cols}) '
                f'VALUES {r_vals} '
                f'ON CONFLICT ({r_uniq_str}) '
                f'DO UPDATE SET {r_updates}'
            )

    def persist_horses(self):
        df = self.clean.pipe(startswith, 'horse__', rename=True)

        cols = ','.join('"{}"'.format(key) for key in df.columns)
        # TODO: Handle null transformations more elegantly
        vals = ','.join(map(str, map(tuple, df.values))) \
            .replace('nan', 'NULL') \
            .replace('None', 'NULL') \
            .replace('\'NaT\'', 'NULL')
        updates = ','.join((f'{key}=excluded.{key}' for key in df.columns))

        sql = (
            f'INSERT INTO horses ({cols}) '
            f'VALUES {vals} '
            f'ON CONFLICT (pedigree_reg_num) '
            f'DO UPDATE SET {updates} '
            f'WHERE horses.jrdb_saved_on IS NULL OR excluded.jrdb_saved_on >= horses.jrdb_saved_on'
        )

        with connection.cursor() as c:
            c.execute(sql)

    @transaction.atomic
    def persist(self):
        # self.persist_races()
        # self.persist_horses()

        for _, row in self.clean.iterrows():
            p = row.pipe(startswith, 'program__', rename=True).dropna().to_dict()
            program, _ = Program.objects.get_or_create(racetrack_id=p.pop('racetrack_id'), yr=p.pop('yr'),
                                                       round=p.pop('round'), day=p.pop('day'))

            r = row.pipe(startswith, 'race__', rename=True).dropna().to_dict()
            race, _ = Race.objects.get_or_create(program=program, num=r.pop('num'))

            h = row.pipe(startswith, 'horse__', rename=True).dropna().to_dict()
            horse, _ = Horse.objects.get_or_create(pedigree_reg_num=h.pop('pedigree_reg_num'), defaults=h)

            try:
                c = row.pipe(startswith, 'contender__', rename=True).dropna().to_dict()
                c['horse_id'] = horse.id
                Contender.objects.update_or_create(race=race, num=c.pop('num'), defaults=c)
            except IntegrityError as e:
                logger.exception(e)
