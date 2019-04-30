import logging

import pandas as pd

from ..models import choices, Program, Race
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

    def persist(self):
        self.upsert('jrdb.Program')

        pdf = self.clean.pipe(startswith, 'program__', rename=True)

        programs = pd.DataFrame(
            Program.objects
                .filter(racetrack_id__in=pdf.racetrack_id, yr__in=pdf.yr, round__in=pdf['round'], day__in=pdf.day)
                .values('id', 'racetrack_id', 'yr', 'round', 'day')
        )
        program_id = pdf.merge(programs).id

        self.upsert('jrdb.Race', program_id=program_id)

        rdf = self.clean.pipe(startswith, 'race__', rename=True)
        races = pd.DataFrame(
            Race.objects
                .filter(program_id__in=program_id, num__in=rdf.num)
                .values('id', 'program_id', 'num')
        )
        rdf['program_id'] = program_id
        race_id = rdf.merge(races, how='left').id

        self.upsert('jrdb.Contender', race_id=race_id)
