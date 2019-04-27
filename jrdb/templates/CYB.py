import logging

import pandas as pd
from django.db import transaction, connection, IntegrityError

from ..models import choices, Program, Race, Contender
from .template import Template, startswith, ProgramRacePersistMixin
from .item import IntegerItem, StringItem, ForeignKeyItem, BooleanItem, ChoiceItem, DateItem

logger = logging.getLogger(__name__)


class CYB(Template, ProgramRacePersistMixin):
    """
    仕様: http://www.jrdb.com/program/Cyb/cyb_doc.txt
    内容説明: http://www.jrdb.com/program/Cyb/cybsiyo_doc.txt
    サンプル: http://www.jrdb.com/program/Cyb/CYB081018.txt
    """
    name = 'JRDB調教分析データ（CYB）'
    items = [
        # レースキー
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('馬番', 2, 8, 'jrdb.Contender.num'),

        ChoiceItem('調教タイプ', 2, 10, 'jrdb.Contender.training_style', choices.TRAINING_STYLE.options()),
        ChoiceItem('調教コース種別', 1, 12, 'jrdb.Contender.training_course_cat', choices.TRAINING_COURSE_CATEGORY.options()),

        # 調教コース種類
        BooleanItem('坂', 2, 13, 'jrdb.Contender.trained_hill', value_true='01', value_false='00'),
        BooleanItem('Ｗ', 2, 15, 'jrdb.Contender.trained_wood_chip', value_true='01', value_false='00'),
        BooleanItem('ダ', 2, 17, 'jrdb.Contender.trained_dirt', value_true='01', value_false='00'),
        BooleanItem('芝', 2, 19, 'jrdb.Contender.trained_turf', value_true='01', value_false='00'),
        BooleanItem('プ', 2, 21, 'jrdb.Contender.trained_pool', value_true='01', value_false='00'),
        BooleanItem('障', 2, 23, 'jrdb.Contender.trained_obstacle', value_true='01', value_false='00'),
        BooleanItem('ポ', 2, 25, 'jrdb.Contender.trained_poly_track', value_true='01', value_false='00'),

        ChoiceItem('調教距離', 1, 27, 'jrdb.Contender.training_distance', choices.TRAINING_DISTANCE.options()),
        ChoiceItem('調教重点', 1, 28, 'jrdb.Contender.training_emphasis', choices.TRAINING_EMPHASIS.options()),
        IntegerItem('追切指数', 3, 29, 'jrdb.Contender.warm_up_time_idx'),
        IntegerItem('仕上指数', 3, 32, 'jrdb.Contender.training_result_idx'),
        ChoiceItem('調教量評価', 1, 35, 'jrdb.Contender.training_amount_eval', choices.TRAINING_AMOUNT_EVAL.options()),
        ChoiceItem('仕上指数変化', 1, 36, 'jrdb.Contender.training_result_idx_change',
                   choices.TRAINING_RESULT_IDX_CHANGE.options()),
        StringItem('調教コメント', 40, 37, 'jrdb.Contender.training_comment'),
        DateItem('コメント年月日', 8, 77, 'jrdb.Contender.training_comment_date'),
        ChoiceItem('調教評価', 1, 85, 'jrdb.Contender.training_evaluation', choices.THREE_STAGE_EVAL.options()),
    ]

    # WIP
    # TODO: Duplicate Contenders exist
    # def persist(self):
    #     super().persist()
    #
    #     sep = ','
    #     r_df = self.clean.pipe(startswith, 'race__', rename=True)
    #     c_df = self.clean.pipe(startswith, 'contender__', rename=True)
    #
    #     r_lookup = {
    #         'program_id__in': r_df.program_id,
    #         'num__in': r_df.num,
    #     }
    #
    #     r_search = Race.objects.filter(**r_lookup).values('id', 'program_id', 'num')
    #     r_search_df = pd.DataFrame(r_search)
    #
    #     c_df['race_id'] = c_df.merge(r_search_df).id
    #
    #     c_cols = sep.join('"{}"'.format(key) for key in c_df.columns)
    #     c_vals = sep.join(map(str, map(tuple, c_df.values))).replace('nan', 'NULL').replace('NaT', 'NULL')
    #
    #     c_uniq = ['race_id', 'num']
    #     c_uniq_str = sep.join('"{}"'.format(key) for key in c_uniq)
    #     c_updates = sep.join((f'{key}=excluded.{key}' for key in c_df.columns if key not in c_uniq))
    #
    #     c_sql = (
    #         f'INSERT INTO contenders ({c_cols}) '
    #         f'VALUES {c_vals} '
    #         f'ON CONFLICT ({c_uniq_str}) '
    #         f'DO UPDATE SET {c_updates}'
    #     )
    #
    #     with connection.cursor() as c:
    #         c.execute(c_sql)

    @transaction.atomic
    def persist(self):
        for _, row in self.clean.iterrows():
            p = row.pipe(startswith, 'program__', rename=True).dropna().to_dict()
            program, _ = Program.objects.get_or_create(racetrack_id=p.pop('racetrack_id'), yr=p.pop('yr'),
                                                       round=p.pop('round'), day=p.pop('day'))

            r = row.pipe(startswith, 'race__', rename=True).dropna().to_dict()
            race, _ = Race.objects.get_or_create(program=program, num=r.pop('num'))

            try:
                c = row.pipe(startswith, 'contender__', rename=True).dropna().to_dict()
                Contender.objects.update_or_create(race=race, num=c.pop('num'), defaults=c)
            except IntegrityError as e:
                logger.exception(e)
