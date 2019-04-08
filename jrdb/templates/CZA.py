import logging

import pandas as pd
from django.db import IntegrityError, transaction

from jrdb.models import choices, Trainer
from jrdb.templates.parse import filter_na, parse_comma_separated_integer_list
from jrdb.templates.template import Template, Item

logger = logging.getLogger(__name__)


class CZA(Template):
    """
    http://www.jrdb.com/program/Cs/Cs_doc1.txt
    """
    name = '全調教師'
    items = [
        Item('jrdb.Trainer.code', '調教師コード', 5, 0),
        Item('is_retired', '登録抹消フラグ', 1, 5, notes='1:抹消,0:現役', use=False),
        Item('jrdb.Trainer.retired_on', '登録抹消年月日', 8, 6, notes='YYYYMMDD', date_fmt='%Y%m%d'),
        Item('jrdb.Trainer.name', '調教師名', 12, 14, notes='全角６文字'),
        Item('jrdb.Trainer.name_kana', '調教師カナ', 30, 26, notes='全角１５文字'),
        Item('jrdb.Trainer.name_abbr', '調教師名略称', 6, 56, notes='全角３文字'),
        Item('jrdb.Trainer.area', '所属コード', 1, 62, notes='1:関東,2:関西,3:他', options=choices.AREA.options()),
        Item('jrdb.Trainer.training_center_name', '所属地域名', 4, 63, notes='全角２文字、地方の場合'),
        Item('jrdb.Trainer.birthday', '生年月日', 8, 67, notes='YYYYMMDD', date_fmt='%Y%m%d'),
        Item('jrdb.Trainer.lic_acquired_yr', '初免許年', 4, 75, notes='YYYY'),
        Item('jrdb.Trainer.jrdb_comment', '調教師コメント', 40, 79, notes='ＪＲＤＢスタッフの厩舎見解'),
        Item('jrdb.Trainer.jrdb_comment_date', 'コメント入力年月日', 8, 119, notes='調教師コメントを入力した年月日', date_fmt='%Y%m%d'),
        Item('jrdb.Trainer.cur_yr_leading', '本年リーディング', 3, 127),
        Item('jrdb.Trainer.cur_yr_flat_r', '本年平地成績', 12, 130, notes='１－２－３－着外(3*4)'),
        Item('jrdb.Trainer.cur_yr_obst_r', '本年障害成績', 12, 142, notes='１－２－３－着外(3*4)'),
        Item('jrdb.Trainer.cur_yr_sp_wins', '本年特別勝数', 3, 154),
        Item('jrdb.Trainer.cur_yr_hs_wins', '本年重賞勝数', 3, 157),
        Item('jrdb.Trainer.prev_yr_leading', '昨年リーディング', 3, 160),
        Item('jrdb.Trainer.prev_yr_flat_r', '昨年平地成績', 12, 163, notes='１－２－３－着外(3*4)'),
        Item('jrdb.Trainer.prev_yr_obst_r', '昨年障害成績', 12, 175, notes='１－２－３－着外(3*4)'),
        Item('jrdb.Trainer.prev_yr_sp_wins', '昨年特別勝数', 3, 187),
        Item('jrdb.Trainer.prev_yr_hs_wins', '昨年重賞勝数', 3, 190),
        Item('jrdb.Trainer.sum_flat_r', '通算平地成績', 20, 193, notes='１－２－３－着外(5*4)'),
        Item('jrdb.Trainer.sum_obst_r', '通算障害成績', 20, 213, notes='１－２－３－着外(5*4)'),
        Item('jrdb.Trainer.jrdb_saved_on', 'データ年月日', 8, 233, notes='YYYYMMDD', date_fmt='%Y%m%d'),
        Item('reserved', '予備', 29, 241, notes='スペース', use=False),
        Item('newline', '改行', 2, 270, notes='ＣＲ・ＬＦ', use=False),
    ]

    def clean(self) -> pd.DataFrame:
        self.df = self.df[~self.df.name.str.contains('削除')]
        return super().clean()

    def clean_cur_yr_flat_r(self):
        return self.df.cur_yr_flat_r.apply(parse_comma_separated_integer_list, args=(3,))

    def clean_cur_yr_obst_r(self):
        return self.df.cur_yr_obst_r.apply(parse_comma_separated_integer_list, args=(3,))

    def clean_prev_yr_flat_r(self):
        return self.df.prev_yr_flat_r.apply(parse_comma_separated_integer_list, args=(3,))

    def clean_prev_yr_obst_r(self):
        return self.df.prev_yr_obst_r.apply(parse_comma_separated_integer_list, args=(3,))

    def clean_sum_flat_r(self):
        return self.df.sum_flat_r.apply(parse_comma_separated_integer_list, args=(5,))

    def clean_sum_obst_r(self):
        return self.df.sum_obst_r.apply(parse_comma_separated_integer_list, args=(5,))

    @transaction.atomic
    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            record = filter_na(row)
            try:
                trainer, created = Trainer.objects.get_or_create(code=record.pop('code'), defaults=record)
                if not created:
                    if trainer.jrdb_saved_on is None or record['jrdb_saved_on'] >= trainer.jrdb_saved_on:
                        for name, value in record.items():
                            setattr(trainer, name, value)
                        trainer.save()
            except IntegrityError as e:
                logger.exception(e)
