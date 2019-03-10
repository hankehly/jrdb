from django.db import models


class SimpleCodeManager(models.Manager):

    def get_by_natural_key(self, key):
        return self.get(key=key)


class SimpleCode(models.Model):
    """
    Common attributes for basic key-value models
    """
    objects = SimpleCodeManager()

    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    class Meta:
        abstract = True


class GradeCode(SimpleCode):
    """
    グレード

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'grade_codes'


class HairColorCode(SimpleCode):
    """
    毛色コード

    栗毛 CHESTNUT
    栃栗 DARK_CHESTNUT
    鹿毛 BAY
    黒鹿 DARK_BAY
    青鹿 BROWN
    青毛 BLACK
    芦毛 GRAY
    栗粕 RED_ROAN
    鹿粕 BAY_ROAN
    青粕 BLUE_ROAN
    白毛 WHITE

    http://www.jrdb.com/program/jrdb_code.txt
    http://home.catv-yokohama.ne.jp/22/hnasb/uma/uma.ryoko/uma.ryo.ke.kasu.html
    http://home.catv-yokohama.ne.jp/22/hnasb/uma/uma.ryoko/uma.ryo.ke.kuri.html
    """

    class Meta:
        db_table = 'hair_color_codes'


class HoofCode(SimpleCode):
    """
    脚元コード

    http://www.jrdb.com/program/ashimoto_code.txt
    """
    value_abbr = models.CharField(max_length=255)

    class Meta:
        db_table = 'hoof_codes'


class HorseBodyCode(SimpleCode):
    """
    馬体コード
    パドックで見た馬体

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'horse_body_codes'


class HorseConditionCode(SimpleCode):
    """
    気配コード
    パドックで見た馬気配

    https://knocchi01.com/2919.html
    http://eigodekeiba.blogspot.com/2016/11/blog-post_12.html

    Note: イレチ = イレ込+チャカつき
    """

    class Meta:
        db_table = 'horse_condition_codes'


class HorseGearCode(SimpleCode):
    """
    馬具コード
    短縮 / 内容

    http://www.jrdb.com/program/bagu_code.txt
    """
    horse_gear_code_category = models.ForeignKey('jrdb.HorseGearCodeCategory', on_delete=models.CASCADE)
    value_abbr = models.CharField(max_length=255)

    class Meta:
        db_table = 'horse_gear_codes'


class HorseGearCodeCategory(SimpleCode):
    """
    馬具種別表

    http://www.jrdb.com/program/bagu_code.txt
    """

    class Meta:
        db_table = 'horse_gear_code_categories'


class HorseSymbol(SimpleCode):
    """
    馬記号コード

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'horse_symbols'


class ImpostClassCode(SimpleCode):
    """
    重量

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'impost_class_codes'


class PaddockObservedHoofCode(SimpleCode):
    """
    蹄コード

    パドックでの観察により馬の蹄を分類したもの。
    各馬の蹄の大きさを大・中・小・細の４種類に、形状を立・標準・標準立・標準ベ・
    ベタの５種類に分類しています。「中ベタ」なら蹄の大きさは中ぐらいでベタ蹄とい
    う意味です。
    芝の重馬場、荒馬場では蹄の立っている馬が有利になります。但しダート戦に関して
    はこの限りではありません。

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'paddock_observed_hoof_codes'


class PenaltyCode(SimpleCode):
    """
    異常区分

    http://www.jrdb.com/program/Sed/sedsiyo_doc.txt
    """

    class Meta:
        db_table = 'penalty_codes'


class RaceCategoryCode(SimpleCode):
    """
    競走種別をコード化

    11　２歳
    12　３歳
    13　３歳以上
    14　４歳以上
    20　障害
    99　その他

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'race_category_codes'


class RaceClass(SimpleCode):
    """
    クラスコード
    馬の能力をクラスで分けたもの。

    芝ＯＰＡ　・・・　芝のオープン戦で勝つ能力のある馬。
    芝ＯＰＢ　・・・　芝のオープン戦で好戦できる能力のある馬。
    芝ＯＰＣ　・・・　芝のオープン戦で頭打ちの馬。

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'race_classes'


class RaceConditionCode(SimpleCode):
    """
    競走条件をコード化

    http://www.jrdb.com/program/jrdb_code.txt
    """
    race_condition_group_code = models.ForeignKey('jrdb.RaceConditionGroupCode', on_delete=models.CASCADE)

    class Meta:
        db_table = 'race_condition_codes'


class RaceConditionGroupCode(SimpleCode):
    """
    条件グループコード
    同クラスの条件をグループ化したコード

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'race_condition_group_codes'


class RacetrackCode(SimpleCode):
    """
    場コード

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'racetrack_codes'


class RacingLineCode(SimpleCode):
    """
    コース取り

    1 最内
    2 内
    3 中
    4 外
    5 大外

    https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1373948028
    """

    class Meta:
        db_table = 'racing_line_codes'


class RestReasonCode(SimpleCode):
    """
    休養理由分類コード

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'rest_reason_codes'


class RunningStyleCode(SimpleCode):
    """
    脚質コード（競走馬が得意とする走り）
    過去の競走実績よりその馬の脚質を判断したコード。
    """

    class Meta:
        db_table = 'running_style_codes'


class SpecialMentionCode(SimpleCode):
    """
    特記コード

    http://www.jrdb.com/program/tokki_code.txt
    """

    class Meta:
        db_table = 'special_mention_codes'


class TrackConditionCode(SimpleCode):
    """
    馬場状態

    http://www.jrdb.com/program/jrdb_code.txt
    https://horseicon.web.fc2.com/track_surface.htm
    """

    class Meta:
        db_table = 'track_condition_codes'


class TrainingCourseCategory(SimpleCode):
    """
    調教コース種別
    調教コースは、トラックを周回する「コース調教」と、「坂路調教」に大別されます。
    ここでは、中間での主な調教コースを示します。

    http://www.jrdb.com/program/Cyb/cybsiyo_doc.txt
    """

    class Meta:
        db_table = 'training_course_categories'


class TrainingStyle(SimpleCode):
    """
    調教タイプ
    調教過程を分析し次のタイプに分類しています。

     ***** 各タイプの調教量と強さの関係表 *****
    　　（軽い）　　　　　　強さ→　　　　　（強い）
    多い┏━━━━━━┳━━━━━━┳━━━━━━┓
    ↑　┃3:乗込　　　┃2:標準多め　┃1:スパルタ　┃
    調　┣━━━━━━╋━━━━━━╋━━━━━━┫
    教　┃6:馬ナリ平均┃5:標準　　　┃4:一杯平均 ┃
    量　┣━━━━━━╋━━━━━━╋━━━━━━┫
    　　┃9:軽目　　　┃8:標準少め　┃7:急仕上げ ┃
    少い┗━━━━━━┻━━━━━━┻━━━━━━┛

    http://www.jrdb.com/program/Cyb/cybsiyo_doc.txt
    """

    class Meta:
        db_table = 'training_styles'


class WeatherCode(SimpleCode):
    """
    天候コード

    http://www.jrdb.com/program/jrdb_code.txt
    """

    class Meta:
        db_table = 'weather_codes'
