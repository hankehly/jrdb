import logging

import pandas as pd
from django.db import connection
from django.utils.functional import cached_property

from ..models import choices
from .item import ChoiceItem, DateItem, ArrayItem, StringItem, IntegerItem
from .template import Template, startswith, PostgresUpsertMixin

logger = logging.getLogger(__name__)


class CZA(Template, PostgresUpsertMixin):
    """
    http://www.jrdb.com/program/Cs/Cs_doc1.txt
    """
    name = '全調教師'
    items = [
        StringItem('調教師コード', 5, 0, 'jrdb.Trainer.code'),
        # 'is_retired', '登録抹消フラグ', width=1, start=5
        DateItem('登録抹消年月日', 8, 6, 'jrdb.Trainer.retired_on'),
        StringItem('調教師名', 12, 14, 'jrdb.Trainer.name'),
        StringItem('調教師カナ', 30, 26, 'jrdb.Trainer.name_kana'),
        StringItem('調教師名略称', 6, 56, 'jrdb.Trainer.name_abbr'),
        ChoiceItem('所属コード', 1, 62, 'jrdb.Trainer.area', choices.AREA.options()),
        StringItem('所属地域名', 4, 63, 'jrdb.Trainer.training_center_name'),
        DateItem('生年月日', 8, 67, 'jrdb.Trainer.birthday'),
        IntegerItem('初免許年', 4, 75, 'jrdb.Trainer.lic_acquired_yr'),
        StringItem('調教師コメント', 40, 79, 'jrdb.Trainer.jrdb_comment'),
        DateItem('コメント入力年月日', 8, 119, 'jrdb.Trainer.jrdb_comment_date'),
        IntegerItem('本年リーディング', 3, 127, 'jrdb.Trainer.cur_yr_leading'),
        ArrayItem('本年平地成績', 12, 130, 'jrdb.Trainer.cur_yr_flat_r', 4),
        ArrayItem('本年障害成績', 12, 142, 'jrdb.Trainer.cur_yr_obst_r', 4),
        IntegerItem('本年特別勝数', 3, 154, 'jrdb.Trainer.cur_yr_sp_wins'),
        IntegerItem('本年重賞勝数', 3, 157, 'jrdb.Trainer.cur_yr_hs_wins'),
        IntegerItem('昨年リーディング', 3, 160, 'jrdb.Trainer.prev_yr_leading'),
        ArrayItem('昨年平地成績', 12, 163, 'jrdb.Trainer.prev_yr_flat_r', 4),
        ArrayItem('昨年障害成績', 12, 175, 'jrdb.Trainer.prev_yr_obst_r', 4),
        IntegerItem('昨年特別勝数', 3, 187, 'jrdb.Trainer.prev_yr_sp_wins'),
        IntegerItem('昨年重賞勝数', 3, 190, 'jrdb.Trainer.prev_yr_hs_wins'),
        ArrayItem('通算平地成績', 20, 193, 'jrdb.Trainer.sum_flat_r', 4),
        ArrayItem('通算障害成績', 20, 213, 'jrdb.Trainer.sum_obst_r', 4),
        DateItem('データ年月日', 8, 233, 'jrdb.Trainer.jrdb_saved_on'),
    ]

    @cached_property
    def clean(self) -> pd.DataFrame:
        self.df = self.df[~self.df['trainer__name'].str.contains('削除')]
        return super().clean

    def persist(self):
        self.upsert(
            symbol='jrdb.Trainer',
            index_predicate='trainers.jrdb_saved_on IS NULL OR excluded.jrdb_saved_on >= trainers.jrdb_saved_on'
        )
