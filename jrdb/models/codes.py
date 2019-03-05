from django.db import models

from jrdb.models import BaseModel


class SimpleCodeManager(models.Manager):
    def get_by_natural_key(self, key):
        return self.get(key=key)


class SimpleCode(BaseModel):
    """
    Common attributes for basic key-value models
    """
    objects = SimpleCodeManager()

    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=255)

    class Meta:
        abstract = True


class RunningStyle(SimpleCode):
    """
    脚質コード（競走馬が得意とする走り）
    過去の競走実績よりその馬の脚質を判断したコード。
    """
    pass


class SpecialMention(SimpleCode):
    """
    特記コード

    http://www.jrdb.com/program/tokki_code.txt
    """
    pass


class HorseGearCategory(SimpleCode):
    """
    馬具種別表

    http://www.jrdb.com/program/bagu_code.txt
    """
    pass


class HorseGearCode(SimpleCode):
    """
    馬具コード
    短縮 / 内容

    http://www.jrdb.com/program/bagu_code.txt
    """
    horse_gear_category = models.ForeignKey('jrdb.HorseGearCategory', on_delete=models.CASCADE)
    value_abbr = models.CharField(max_length=255)


class HorseSymbol(SimpleCode):
    """
    馬記号コード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    pass


class RaceTrack(SimpleCode):
    """
    場コード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    pass


class TrackCondition(SimpleCode):
    """
    馬場状態

    http://www.jrdb.com/program/jrdb_code.txt
    https://horseicon.web.fc2.com/track_surface.htm
    """
    pass


class Impost(SimpleCode):
    """
    重量

    http://www.jrdb.com/program/jrdb_code.txt
    """
    pass


class Grade(SimpleCode):
    """
    グレード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    pass


class HorseCondition(SimpleCode):
    """
    気配コード
    パドックで見た馬気配

    https://knocchi01.com/2919.html
    http://eigodekeiba.blogspot.com/2016/11/blog-post_12.html

    Note: イレチ = イレ込+チャカつき
    """
    pass


class RacingLine(SimpleCode):
    """
    コース取り

    1 最内
    2 内
    3 中
    4 外
    5 大外

    https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1373948028
    """
    pass


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
    pass


class TrainingCourseCategory(SimpleCode):
    """
    調教コース種別
    調教コースは、トラックを周回する「コース調教」と、「坂路調教」に大別されます。
    ここでは、中間での主な調教コースを示します。

    http://www.jrdb.com/program/Cyb/cybsiyo_doc.txt
    """
    pass


class Weather(SimpleCode):
    """
    天候コード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    pass


class RestReason(SimpleCode):
    """
    休養理由分類コード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    pass


class HairColor(SimpleCode):
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
    pass


class HorseBody(SimpleCode):
    """
    馬体コード
    パドックで見た馬体

    http://www.jrdb.com/program/jrdb_code.txt
    """
    pass


class RaceClass(SimpleCode):
    """
    クラスコード
    馬の能力をクラスで分けたもの。

    芝ＯＰＡ　・・・　芝のオープン戦で勝つ能力のある馬。
    芝ＯＰＢ　・・・　芝のオープン戦で好戦できる能力のある馬。
    芝ＯＰＣ　・・・　芝のオープン戦で頭打ちの馬。

    http://www.jrdb.com/program/jrdb_code.txt
    """
    pass


class PaddockObservedHoff(SimpleCode):
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
    pass


class HoofCode(SimpleCode):
    """
    脚元コード

    http://www.jrdb.com/program/ashimoto_code.txt
    """
    value_abbr = models.CharField(max_length=255)
