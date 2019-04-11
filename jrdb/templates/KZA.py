import logging

from django.db import IntegrityError, transaction

from jrdb.models import Jockey, Trainer, choices
from jrdb.templates.parse import filter_na
from jrdb.templates.template import Template
from jrdb.templates.item import StringItem, DateItem, ChoiceItem, IntegerItem, ForeignKeyItem, ArrayItem

logger = logging.getLogger(__name__)


class KZA(Template):
    """
    http://www.jrdb.com/program/Ks/Ks_doc1.txt
    """
    name = '全騎手'
    items = [
        StringItem('騎手コード', 5, 0, 'jrdb.Jockey.code'),
        # 'is_retired', '登録抹消フラグ', width=1, start=5
        DateItem('登録抹消年月日', 8, 6, 'jrdb.Jockey.retired_on'),
        StringItem('騎手名', 12, 14, 'jrdb.Jockey.name'),
        StringItem('騎手カナ', 30, 26, 'jrdb.Jockey.name_kana'),
        StringItem('騎手名略称', 6, 56, 'jrdb.Jockey.name_abbr'),
        ChoiceItem('所属コード', 1, 62, 'jrdb.Jockey.area', choices.AREA.options()),
        StringItem('所属地域名', 4, 63, 'jrdb.Jockey.training_center_name'),
        DateItem('生年月日', 8, 67, 'jrdb.Jockey.birthday'),
        IntegerItem('初免許年', 4, 75, 'jrdb.Jockey.lic_acquired_yr'),
        ChoiceItem('見習い区分', 1, 79, 'jrdb.Jockey.trainee_cat', choices.TRAINEE_CATEGORY.options()),
        ForeignKeyItem('所属厩舎', 5, 80, 'jrdb.Jockey.trainer', 'jrdb.Trainer.code'),
        StringItem('騎手コメント', 40, 85, 'jrdb.Jockey.jrdb_comment'),
        DateItem('コメント入力年月日', 8, 125, 'jrdb.Jockey.jrdb_comment_date'),
        IntegerItem('本年リーディング', 3, 133, 'jrdb.Jockey.cur_yr_leading'),
        ArrayItem('本年平地成績', 12, 136, 'jrdb.Jockey.cur_yr_flat_r', 4),
        ArrayItem('本年障害成績', 12, 148, 'jrdb.Jockey.cur_yr_obst_r', 4),
        IntegerItem('本年特別勝数', 3, 160, 'jrdb.Jockey.cur_yr_sp_wins'),
        IntegerItem('本年重賞勝数', 3, 163, 'jrdb.Jockey.cur_yr_hs_wins'),
        IntegerItem('昨年リーディング', 3, 166, 'jrdb.Jockey.prev_yr_leading'),
        ArrayItem('昨年平地成績', 12, 169, 'jrdb.Jockey.prev_yr_flat_r', 4),
        ArrayItem('昨年障害成績', 12, 181, 'jrdb.Jockey.prev_yr_obst_r', 4),
        IntegerItem('昨年特別勝数', 3, 193, 'jrdb.Jockey.prev_yr_sp_wins'),
        IntegerItem('昨年重賞勝数', 3, 196, 'jrdb.Jockey.prev_yr_hs_wins'),
        ArrayItem('通算平地成績', 20, 199, 'jrdb.Jockey.sum_flat_r', 4),
        ArrayItem('通算障害成績', 20, 219, 'jrdb.Jockey.sum_obst_r', 4),
        DateItem('データ年月日', 8, 239, 'jrdb.Jockey.jrdb_saved_on')
    ]

    def clean(self):
        self.df = self.df[~self.df.name.str.contains('削除')]
        return super().clean()

    @transaction.atomic
    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            record = filter_na(row)
            try:
                # trainer_code is changed to trainer_id during ForeignKeyItem.clean
                # and trainer_id is nan because there is no trainer
                # we want to create the related records during persist
                if record.get('trainer_code'):
                    trainer, _ = Trainer.objects.get_or_create(code=record.pop('trainer_code'))
                    record['trainer_id'] = trainer.id
                jockey, created = Jockey.objects.get_or_create(code=record.pop('code'), defaults=record)
                if not created:
                    if jockey.jrdb_saved_on is None or record['jrdb_saved_on'] >= jockey.jrdb_saved_on:
                        for name, value in record.items():
                            setattr(jockey, name, value)
                        jockey.save()
            except IntegrityError as e:
                logger.exception(e)
