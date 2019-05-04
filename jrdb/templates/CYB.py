from ..models import choices
from .template import Template, startswith
from .item import IntegerItem, StringItem, ForeignKeyItem, BooleanItem, ChoiceItem, DateItem


class CYB(Template):
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

    def load(self):
        pdf = self.transform.pipe(startswith, 'program__', rename=True)
        programs = self.loader_cls(pdf, 'jrdb.Program').load().to_dataframe()

        rdf = self.transform.pipe(startswith, 'race__', rename=True)
        rdf['program_id'] = pdf.merge(programs, how='left').id
        races = self.loader_cls(rdf, 'jrdb.Race').load().to_dataframe()

        cdf = self.transform.pipe(startswith, 'contender__', rename=True)
        cdf['race_id'] = rdf[['program_id', 'num']].merge(races, how='left').id

        self.loader_cls(cdf, 'jrdb.Contender').load()
