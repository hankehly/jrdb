import logging

from django.db import IntegrityError, transaction

from jrdb.models import Jockey, Trainer, choices
from jrdb.templates.parse import filter_na, parse_comma_separated_integer_list
from jrdb.templates.template import Template, Item, DateItem, ChoiceItem

logger = logging.getLogger(__name__)


class KZA(Template):
    """
    http://www.jrdb.com/program/Ks/Ks_doc1.txt
    """
    name = '全騎手'
    items = [
        Item('jrdb.Jockey.code', '騎手コード', 5, 0),
        Item('is_retired', '登録抹消フラグ', 1, 5, drop=True),
        DateItem('jrdb.Jockey.retired_on', '登録抹消年月日', 8, 6),
        Item('jrdb.Jockey.name', '騎手名', 12, 14),
        Item('jrdb.Jockey.name_kana', '騎手カナ', 30, 26),
        Item('jrdb.Jockey.name_abbr', '騎手名略称', 6, 56),
        ChoiceItem('jrdb.Jockey.area', '所属コード', 1, 62, options=choices.AREA.options()),
        Item('jrdb.Jockey.training_center_name', '所属地域名', 4, 63),
        DateItem('jrdb.Jockey.birthday', '生年月日', 8, 67),
        Item('jrdb.Jockey.lic_acquired_yr', '初免許年', 4, 75),
        ChoiceItem('jrdb.Jockey.trainee_cat', '見習い区分', 1, 79, options=choices.TRAINEE_CATEGORY.options()),
        Item('jrdb.Jockey.trainer.code', '所属厩舎', 5, 80),
        Item('jrdb.Jockey.jrdb_comment', '騎手コメント', 40, 85),
        DateItem('jrdb.Jockey.jrdb_comment_date', 'コメント入力年月日', 8, 125),
        Item('jrdb.Jockey.cur_yr_leading', '本年リーディング', 3, 133),
        Item('jrdb.Jockey.cur_yr_flat_r', '本年平地成績', 12, 136),
        Item('jrdb.Jockey.cur_yr_obst_r', '本年障害成績', 12, 148),
        Item('jrdb.Jockey.cur_yr_sp_wins', '本年特別勝数', 3, 160),
        Item('jrdb.Jockey.cur_yr_hs_wins', '本年重賞勝数', 3, 163),
        Item('jrdb.Jockey.prev_yr_leading', '昨年リーディング', 3, 166),
        Item('jrdb.Jockey.prev_yr_flat_r', '昨年平地成績', 12, 169),
        Item('jrdb.Jockey.prev_yr_obst_r', '昨年障害成績', 12, 181),
        Item('jrdb.Jockey.prev_yr_sp_wins', '昨年特別勝数', 3, 193),
        Item('jrdb.Jockey.prev_yr_hs_wins', '昨年重賞勝数', 3, 196),
        Item('jrdb.Jockey.sum_flat_r', '通算平地成績', 20, 199),
        Item('jrdb.Jockey.sum_obst_r', '通算障害成績', 20, 219),
        DateItem('jrdb.Jockey.jrdb_saved_on', 'データ年月日', 8, 239),
        Item('reserved', '予備', 23, 247, drop=True),
        Item('newline', '改行', 2, 270, drop=True),
    ]

    def clean(self):
        self.df = self.df[~self.df['jrdb.Jockey.name'].str.contains('削除')]
        return super().clean()

    def clean_cur_yr_flat_r(self):
        return self.df['jrdb.Jockey.cur_yr_flat_r'].apply(parse_comma_separated_integer_list, args=(3,))

    def clean_cur_yr_obst_r(self):
        return self.df['jrdb.Jockey.cur_yr_obst_r'].apply(parse_comma_separated_integer_list, args=(3,))

    def clean_prev_yr_flat_r(self):
        return self.df['jrdb.Jockey.prev_yr_flat_r'].apply(parse_comma_separated_integer_list, args=(3,))

    def clean_prev_yr_obst_r(self):
        return self.df['jrdb.Jockey.prev_yr_obst_r'].apply(parse_comma_separated_integer_list, args=(3,))

    def clean_sum_flat_r(self):
        return self.df['jrdb.Jockey.sum_flat_r'].apply(parse_comma_separated_integer_list, args=(5,))

    def clean_sum_obst_r(self):
        return self.df['jrdb.Jockey.sum_obst_r'].apply(parse_comma_separated_integer_list, args=(5,))

    @transaction.atomic
    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            record = filter_na(row)

            try:
                if 'jrdb.Jockey.trainer.code' in record:
                    trainer, _ = Trainer.objects.get_or_create(code=record.pop('jrdb.Jockey.trainer.code'))
                    record['trainer_id'] = trainer.id

                jockey, created = Jockey.objects.get_or_create(code=record.pop('jrdb.Jockey.code'), defaults=record)
                if not created:
                    if jockey.jrdb_saved_on is None or record['jrdb.Jockey.jrdb_saved_on'] >= jockey.jrdb_saved_on:
                        for name, value in record.items():
                            setattr(jockey, name, value)
                        jockey.save()
            except IntegrityError as e:
                logger.exception(e)
