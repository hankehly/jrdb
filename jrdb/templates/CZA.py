import re
from datetime import datetime

from django.db import IntegrityError
import numpy as np

from jrdb.models.trainer import Trainer
from jrdb.templates.parse import parse_date, parse_int_or, parse_comma_separated_integer_list, filter_na
from jrdb.templates.template import Template


class CZA(Template):
    """
    http://www.jrdb.com/program/Cs/Cs_doc1.txt
    """
    name = '全調教師'
    items = [
        ['code', '調教師コード', None, '5', '99999', '1', None],
        ['is_retired', '登録抹消フラグ', None, '1', '9', '6', '1:抹消,0:現役'],
        ['retired_on', '登録抹消年月日', None, '8', '9', '7', 'YYYYMMDD'],
        ['name', '調教師名', None, '12', 'X', '15', '全角６文字'],
        ['name_kana', '調教師カナ', None, '30', 'X', '27', '全角１５文字'],
        ['name_abbr', '調教師名略称', None, '6', 'X', '57', '全角３文字'],
        ['area', '所属コード', None, '1', '9', '63', '1:関東,2:関西,3:他'],
        ['training_center_name', '所属地域名', None, '4', 'X', '64', '全角２文字、地方の場合'],
        ['birthday', '生年月日', None, '8', '9', '68', 'YYYYMMDD'],
        ['lic_acquired_yr', '初免許年', None, '4', '9', '76', 'YYYY'],
        ['jrdb_comment', '調教師コメント', None, '40', 'X', '80', 'ＪＲＤＢスタッフの厩舎見解'],
        ['jrdb_comment_date', 'コメント入力年月日', None, '8', 'X', '120', '調教師コメントを入力した年月日'],
        ['cur_yr_rtg', '本年リーディング', None, '3', 'ZZ9', '128', None],
        ['cur_yr_flat_r', '本年平地成績', None, '12', 'ZZ9*4', '131', '１－２－３－着外(3*4)'],
        ['cur_yr_obst_r', '本年障害成績', None, '12', 'ZZ9*4', '143', '１－２－３－着外(3*4)'],
        ['cur_yr_sp_wins', '本年特別勝数', None, '3', 'ZZ9', '155', None],
        ['cur_yr_hs_wins', '本年重賞勝数', None, '3', 'ZZ9', '158', None],
        ['prev_yr_rtg', '昨年リーディング', None, '3', 'ZZ9', '161', None],
        ['prev_yr_flat_r', '昨年平地成績', None, '12', 'ZZ9*4', '164', '１－２－３－着外(3*4)'],
        ['prev_yr_obst_r', '昨年障害成績', None, '12', 'ZZ9*4', '176', '１－２－３－着外(3*4)'],
        ['prev_yr_sp_wins', '昨年特別勝数', None, '3', 'ZZ9', '188', None],
        ['prev_yr_hs_wins', '昨年重賞勝数', None, '3', 'ZZ9', '191', None],
        ['sum_flat_r', '通算平地成績', None, '20', 'ZZZZ9*4', '194', '１－２－３－着外(5*4)'],
        ['sum_obst_r', '通算障害成績', None, '20', 'ZZZZ9*4', '214', '１－２－３－着外(5*4)'],
        ['saved_on', 'データ年月日', None, '8', '9', '234', 'YYYYMMDD'],  # same date as filename
        ['reserved', '予備', None, '29', 'X', '242', 'スペース'],
        ['newline', '改行', None, '2', 'X', '271', 'ＣＲ・ＬＦ']
    ]

    def clean(self):
        df = self.df.drop(columns=['is_retired', 'training_center_name', 'saved_on', 'reserved', 'newline'])

        df.name = df.name.str.strip()
        df.name_kana = df.name_kana.str.strip()
        df.name_abbr = df.name_abbr.str.strip()

        df.retired_on = df.retired_on.apply(parse_date, args=('%Y%m%d',))
        df.area = df.area.astype(int).map({1: Trainer.KANTOU, 2: Trainer.KANSAI, 3: Trainer.OTHER})
        df.birthday = df.birthday.apply(parse_date, args=('%Y%m%d',))
        df.lic_acquired_yr = df.lic_acquired_yr.astype(int)
        df.jrdb_comment = df.jrdb_comment.str.strip()
        df.jrdb_comment_date = df.jrdb_comment_date.apply(parse_date, args=('%Y%m%d',))

        df.cur_yr_rtg = df.cur_yr_rtg.str.strip().apply(parse_int_or, args=(np.nan,)).astype('Int64')
        df.cur_yr_flat_r = df.cur_yr_flat_r.apply(parse_comma_separated_integer_list, args=(3,))
        df.cur_yr_obst_r = df.cur_yr_obst_r.apply(parse_comma_separated_integer_list, args=(3,))
        df.cur_yr_sp_wins = df.cur_yr_sp_wins.str.strip().apply(parse_int_or, args=(0,)).astype(int)
        df.cur_yr_hs_wins = df.cur_yr_hs_wins.str.strip().apply(parse_int_or, args=(0,)).astype(int)

        df.prev_yr_rtg = df.prev_yr_rtg.str.strip().apply(parse_int_or, args=(np.nan,)).astype('Int64')
        df.prev_yr_flat_r = df.prev_yr_flat_r.apply(parse_comma_separated_integer_list, args=(3,))
        df.prev_yr_obst_r = df.prev_yr_obst_r.apply(parse_comma_separated_integer_list, args=(3,))
        df.prev_yr_sp_wins = df.prev_yr_sp_wins.str.strip().apply(parse_int_or, args=(0,)).astype(int)
        df.prev_yr_hs_wins = df.prev_yr_hs_wins.str.strip().apply(parse_int_or, args=(0,)).astype(int)

        df.sum_flat_r = df.sum_flat_r.apply(parse_comma_separated_integer_list, args=(5,))
        df.sum_obst_r = df.sum_obst_r.apply(parse_comma_separated_integer_list, args=(5,))

        return df

    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            obj = filter_na(row)
            try:
                Trainer.objects.create(**obj)
            except IntegrityError:
                Trainer.objects.filter(code=obj['code']).update(**obj)
