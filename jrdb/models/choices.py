class SIMPLE_CHOICE:
    CONFIG = ()
    CHOICES = ((t[1], t[2]) for t in CONFIG)
    MAP = {t[0]: t[1] for t in CONFIG}


class GRADE(SIMPLE_CHOICE):
    """
    グレード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    G1 = 'G1'
    G2 = 'G2'
    G3 = 'G3'
    HIGH_STAKES = 'HIGH_STAKES'
    SPECIAL = 'SPECIAL'
    LISTED = 'LISTED'
    CONFIG = (
        ('1', G1, 'Ｇ１'),
        ('2', G2, 'Ｇ２'),
        ('3', G3, 'Ｇ３'),
        ('4', HIGH_STAKES, '重賞'),
        ('5', SPECIAL, '特別'),
        ('6', LISTED, 'Ｌ（リステッド競走）')
    )


class DEMEANOR(SIMPLE_CHOICE):
    """
    気配コード
    パドックで見た馬気配

    https://knocchi01.com/2919.html
    http://eigodekeiba.blogspot.com/2016/11/blog-post_12.html
    """
    GOOD_CONDITION = 'GOOD_CONDITION'
    NORMAL = 'NORMAL'
    UNSTABLE = 'UNSTABLE'
    EXCITED = 'EXCITED'
    GOOD_SPIRIT = 'GOOD_SPIRIT'
    LACKING_SPIRIT = 'LACKING_SPIRIT'
    RESTLESS = 'RESTLESS'
    EXCITED_AND_RESTLESS = 'EXCITED_AND_RESTLESS'
    CONFIG = (
        ('1', GOOD_CONDITION, '状態良'),
        ('2', NORMAL, '平凡'),
        ('3', UNSTABLE, '不安定'),
        ('4', EXCITED, 'イレ込'),
        ('5', GOOD_SPIRIT, '気合良'),
        ('6', LACKING_SPIRIT, '気不足'),
        ('7', RESTLESS, 'チャカ'),
        ('8', EXCITED_AND_RESTLESS, 'イレチ（イレ込+チャカつき）')
    )


class PHYSIQUE(SIMPLE_CHOICE):
    """
    馬体コード
    パドックで見た馬体

    http://www.jrdb.com/program/jrdb_code.txt
    http://d.hatena.ne.jp/Southend/20100809/p1
    https://ameblo.jp/carrot-myhorse-from2012/entry-12282629630.html
    http://www.geocities.jp/wins_weekends/before/beginers/pad-siag.html
    """
    FAT = 'FAT'
    OVERWEIGHT = 'OVERWEIGHT'
    GOOD = 'GOOD'
    NORMAL = 'NORMAL'
    THIN = 'THIN'
    FRESH = 'FRESH'
    LOOSE = 'LOOSE'
    CONFIG = (
        ('1', FAT, '太い'),
        ('2', OVERWEIGHT, '余裕'),
        ('3', GOOD, '良い'),
        ('4', NORMAL, '普通'),
        ('5', THIN, '細い'),
        ('6', FRESH, '張り'),
        ('7', LOOSE, '緩い')
    )


class HORSE_SYMBOL(SIMPLE_CHOICE):
    """
    馬記号コード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    CHOICES = (
        ('01', '○抽'),
        ('02', '□抽'),
        ('03', '○父'),
        ('04', '○市'),
        ('05', '○地'),
        ('06', '○外'),
        ('07', '○父○抽'),
        ('08', '○父○市'),
        ('09', '○父○地'),
        ('10', '○市○地'),
        ('11', '○外○地'),
        ('12', '○父○市○地'),
        ('15', '○招'),
        ('16', '○招○外'),
        ('17', '○招○父'),
        ('18', '○招○市'),
        ('19', '○招○父○市'),
        ('20', '○父○外'),
        ('21', '□地'),
        ('22', '○外□地'),
        ('23', '○父□地'),
        ('24', '○市□地'),
        ('25', '○父○市□地'),
        ('26', '□外'),
        ('27', '○父□外')
    )


class IMPOST_CLASS(SIMPLE_CHOICE):
    """
    重量

    http://www.jrdb.com/program/jrdb_code.txt
    http://cattle.x-winz.net/edb2_manual/12-3-99-CODE.html#C2008
    """
    HANDICAP = 'HANDICAP'
    SPECIAL_WEIGHT = 'SPECIAL_WEIGHT'
    WEIGHT_FOR_AGE = 'WEIGHT_FOR_AGE'
    SPECIAL_WEIGHT_AGE_SEX = 'SPECIAL_WEIGHT_AGE_SEX'
    CONFIG = (
        ('1', HANDICAP, 'ハンデ'),
        ('2', SPECIAL_WEIGHT, '別定'),
        ('3', WEIGHT_FOR_AGE, '馬齢'),
        ('4', SPECIAL_WEIGHT_AGE_SEX, '定量')
    )


class IMPROVEMENT(SIMPLE_CHOICE):
    """
    上昇度

    1 AA かなりの上積みが期待でき、勝つ可能性は高い。
    2  A まずまずの上積みが望め、好勝負ができる。
    3  B 次走も同じ様な状態でレースに挑む。
    4  C ギリギリの仕上げであったため、次走はガタの来そうな気配。
    5  ? 調子落ちの傾向、厳しいレースになる。
    """
    AA = 'AA'
    A = 'A'
    B = 'B'
    C = 'C'
    Q = '?'
    CONFIG = (
        ('1', AA, 'AA'),
        ('2', A, 'A'),
        ('3', B, 'B'),
        ('4', C, 'C'),
        ('5', Q, '?')
    )


class PADDOCK_OBSERVED_HOOF(SIMPLE_CHOICE):
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
    CHOICES = (
        ('01', '大ベタ'),
        ('02', '中ベタ'),
        ('03', '小ベタ'),
        ('04', '細ベタ'),
        ('05', '大立'),
        ('06', '中立'),
        ('07', '小立'),
        ('08', '細立'),
        ('09', '大標準'),
        ('10', '中標準'),
        ('11', '小標準'),
        ('12', '細標準'),
        ('17', '大標起'),
        ('18', '中標起'),
        ('19', '小標起'),
        ('20', '細標起'),
        ('21', '大標ベ'),
        ('22', '中標ベ'),
        ('23', '小標ベ'),
        ('24', '細標ベ')
    )


class PENALTY(SIMPLE_CHOICE):
    """
    異常区分

    http://www.jrdb.com/program/Sed/sedsiyo_doc.txt
    """
    NORMAL = 'NORMAL'
    SCRATCHED = 'SCRATCHED'
    EXCLUDED = 'EXCLUDED'
    FAIL_TO_FINISH = 'FAIL_TO_FINISH'
    DISQUALIFIED = 'DISQUALIFIED'
    DISQUALIFIED_AND_PLACED = 'DISQUALIFIED_AND_PLACED'
    REMOUNT = 'REMOUNT'
    CONFIG = (
        ('0', NORMAL, '異常なし'),
        ('1', SCRATCHED, '取消'),
        ('2', EXCLUDED, '除外'),
        ('3', FAIL_TO_FINISH, '中止'),
        ('4', DISQUALIFIED, '失格'),
        ('5', DISQUALIFIED_AND_PLACED, '降着'),
        ('6', REMOUNT, '再騎乗')
    )


class PACE_CATEGORY(SIMPLE_CHOICE):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    SLOW = 'SLOW'
    CONFIG = (
        ('H', HIGH, 'ハイ'),
        ('M', MEDIUM, '平均'),
        ('S', SLOW, 'スロー')
    )


class RACE_CATEGORY(SIMPLE_CHOICE):
    """
    競走種別をコード化

    http://www.jrdb.com/program/jrdb_code.txt
    """
    TWO_YR_OLD = 'TWO_YR_OLD'
    THREE_YR_OLD = 'THREE_YR_OLD'
    THREE_YR_OLD_AND_UP = 'THREE_YR_OLD_AND_UP'
    FOUR_YR_OLD_AND_UP = 'FOUR_YR_OLD_AND_UP'
    OBSTACLE = 'OBSTACLE'
    OTHER = 'OTHER'
    CONFIG = (
        ('11', TWO_YR_OLD, '2歳'),
        ('12', THREE_YR_OLD, '3歳'),
        ('13', THREE_YR_OLD_AND_UP, '3歳以上'),
        ('14', FOUR_YR_OLD_AND_UP, '4歳以上'),
        ('20', OBSTACLE, '障害'),
        ('99', OTHER, 'その他')
    )


class RACE_LINE(SIMPLE_CHOICE):
    """
    コース取り

    https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1373948028
    """
    INNERMOST = 'INNERMOST'
    INNER = 'INNER'
    MIDDLE = 'MIDDLE'
    OUTER = 'OUTER'
    OUTERMOST = 'OUTERMOST'
    CONFIG = (
        ('1', INNERMOST, '最内'),
        ('2', INNER, '内'),
        ('3', MIDDLE, '中'),
        ('4', OUTER, '外'),
        ('5', OUTERMOST, '大外')
    )


class RACE_HORSE_SEX_SYMBOL(SIMPLE_CHOICE):
    """
    ２桁目　馬の性別による条件
        0　なし
        1　牡馬限定
        2　牝馬限定
        3　牡・せん馬限定
        4　牡・牝馬限定
    """
    NA = 'NA'
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    MALE_CASTRATED = 'MALE_CASTRATED'
    FEMALE_CASTRATED = 'FEMALE_CASTRATED'
    CONFIG = (
        ('0', NA, 'なし'),
        ('1', MALE, '牡馬限定'),
        ('2', FEMALE, '牝馬限定'),
        ('3', MALE_CASTRATED, '牡・せん馬限定'),
        ('4', FEMALE_CASTRATED, '牡・牝馬限定')
    )


class RACE_HORSE_TYPE_SYMBOL(SIMPLE_CHOICE):
    """
    競走記号をコード化

    １桁目　馬の種類による条件
        0　なし
        1　○混
            （混合）性別は混合ということ
        2　○父
            （まるちち）日本で生産された馬を父親に持つ馬。正式には父内国産馬という）
        3　○市○抽
            （まるいち）セリ市で売買された抽選馬を除く馬。正式には市場取引馬という。
            （まるちゅう）ＪＲＡがセリ市で購入して育成した馬で希望する馬主に抽選で売却された馬。
        4　九州産限定 - 九州地方で生産された競走馬のこと
        5　○国際混

    http://www.jrdb.com/program/jrdb_code.txt
    http://cattle.x-winz.net/edb2_manual/12-3-99-CODE.html#C2006
    """
    NA = 'NA'
    MIX = 'MIX'
    D = '(D)'
    KYU = 'KYU'
    A_S = '(A)(S)'
    INT = 'INT'
    CONFIG = (
        ('0', NA, 'なし'),
        ('1', MIX, '○混'),
        ('2', D, '○父'),
        ('3', A_S, '○市○抽'),
        ('4', KYU, '九州産限定'),
        ('5', INT, '○国際混')
    )


class RACE_INTERLEAGUE_SYMBOL(SIMPLE_CHOICE):
    """
    競走記号をコード化

    ３桁目　交流競走の指定
        0　なし
        1　○指
        2　□指
        3　○特指
        4　若手
    """
    NA = 'NA'
    DSN = 'DSN'
    DES = 'DES'
    SD = 'SD'
    JUNIOR = 'JUNIOR'
    CONFIG = (
        ('0', NA, 'なし'),
        ('1', DSN, '○指'),
        ('2', DES, '□指'),
        ('3', SD, '○特指'),
        ('4', JUNIOR, '若手')
    )


class REST_REASON(SIMPLE_CHOICE):
    """
    休養理由分類コード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    CHOICES = (
        ('01', '放牧'),
        ('02', '放牧(故障、骨折等)'),
        ('03', '放牧(不安、ソエ等)'),
        ('04', '放牧(病気)'),
        ('05', '放牧(再審査)'),
        ('06', '放牧(出走停止)'),
        ('07', '放牧(手術）'),
        ('11', '調整'),
        ('12', '調整(故障、骨折等)'),
        ('13', '調整(不安、ソエ等)'),
        ('14', '調整(病気)')
    )


class RUNNING_STYLE(SIMPLE_CHOICE):
    """
    脚質コード（競走馬が得意とする走り）
    過去の競走実績よりその馬の脚質を判断したコード。
    """
    FRONT_RUNNER = 'FRONT_RUNNER'
    STALKER = 'STALKER'
    OTP = 'OTP'  # Off the pace
    OTP_STRETCH = 'OTP_STRETCH'
    OTP_GOOD_POS = 'OTP_GOOD_POS'
    VERSATILE = 'VERSATILE'
    CONFIG = (
        ('1', FRONT_RUNNER, '逃げ'),
        ('2', STALKER, '先行'),
        ('3', OTP, '差し'),
        ('4', OTP_STRETCH, '追込'),
        ('5', OTP_GOOD_POS, '好位差し'),
        ('6', VERSATILE, '自在')
    )


class TRACK_CONDITION(SIMPLE_CHOICE):
    """
    馬場状態

    http://www.jrdb.com/program/jrdb_code.txt
    https://horseicon.web.fc2.com/track_surface.htm
    """
    FIRM = 'FIRM'
    FIRM_FAST = 'FIRM_FAST'
    FIRM_SLOW = 'FIRM_SLOW'
    GOOD = 'GOOD'
    GOOD_FAST = 'GOOD_FAST'
    GOOD_SLOW = 'GOOD_SLOW'
    YIELDING = 'YIELDING'
    YIELDING_FAST = 'YIELDING_FAST'
    YIELDING_SLOW = 'YIELDING_SLOW'
    SOFT = 'SOFT'
    SOFT_FAST = 'SOFT_FAST'
    SOFT_SLOW = 'SOFT_SLOW'
    CONFIG = (
        ('10', FIRM, '良'),
        ('11', FIRM_FAST, '速良'),
        ('12', FIRM_SLOW, '遅良'),
        ('20', GOOD, '稍重'),
        ('21', GOOD_FAST, '速稍重'),
        ('22', GOOD_SLOW, '遅稍重'),
        ('30', YIELDING, '重'),
        ('31', YIELDING_FAST, '速重'),
        ('32', YIELDING_SLOW, '遅重'),
        ('40', SOFT, '不良'),
        ('41', SOFT_FAST, '速不良'),
        ('42', SOFT_SLOW, '遅不良')
    )


class TRAINING_COURSE_CATEGORY(SIMPLE_CHOICE):
    """
    調教コース種別
    調教コースは、トラックを周回する「コース調教」と、「坂路調教」に大別されます。
    ここでは、中間での主な調教コースを示します。

    http://www.jrdb.com/program/Cyb/cybsiyo_doc.txt
    """
    CHOICES = (
        ('1', '坂路調教'),
        ('2', 'コース調教'),
        ('3', '併用(坂路、コース併用)'),
        ('4', '障害（障害練習）'),
        ('5', '障害他（障害練習＋α）'),
        ('0', '他（調教なし、不明）')
    )


class TRAINING_STYLE(SIMPLE_CHOICE):
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
    CHOICES = (
        ('01', 'スパルタ'),
        ('02', '標準多め'),
        ('03', '乗込'),
        ('04', '一杯平均'),
        ('05', '標準'),
        ('06', '馬ナリ平均'),
        ('07', '急仕上げ'),
        ('08', '標準少め'),
        ('09', '軽目'),
        ('10', '連闘'),
        ('11', '調教なし')
    )


class HAIR_COLOR(SIMPLE_CHOICE):
    """
    毛色コード

    http://www.jrdb.com/program/jrdb_code.txt
    http://home.catv-yokohama.ne.jp/22/hnasb/uma/uma.ryoko/uma.ryo.ke.kasu.html
    http://home.catv-yokohama.ne.jp/22/hnasb/uma/uma.ryoko/uma.ryo.ke.kuri.html
    """
    CHESTNUT = 'CHESTNUT'
    DARK_CHESTNUT = 'DARK_CHESTNUT'
    BAY = 'BAY'
    DARK_BAY = 'DARK_BAY'
    BROWN = 'BROWN'
    BLACK = 'BLACK'
    GRAY = 'GRAY'
    RED_ROAN = 'RED_ROAN'
    BAY_ROAN = 'BAY_ROAN'
    BLUE_ROAN = 'BLUE_ROAN'
    WHITE = 'WHITE'
    CONFIG = (
        ('01', CHESTNUT, '栗毛'),
        ('02', DARK_CHESTNUT, '栃栗'),
        ('03', BAY, '鹿毛'),
        ('04', DARK_BAY, '黒鹿'),
        ('05', BROWN, '青鹿'),
        ('06', BLACK, '青毛'),
        ('07', GRAY, '芦毛'),
        ('08', RED_ROAN, '栗粕'),
        ('09', BAY_ROAN, '鹿粕'),
        ('10', BLUE_ROAN, '青粕'),
        ('11', WHITE, '白毛')
    )


class WEATHER(SIMPLE_CHOICE):
    """
    天候コード
    1 晴
    2 曇
    3 小雨
    4 雨
    5 小雪
    6 雪

    http://www.jrdb.com/program/jrdb_code.txt
    """
    FINE = 'FINE'
    CLOUDY = 'CLOUDY'
    DRIZZLE = 'DRIZZLE'
    RAINY = 'RAINY'
    LIGHT_SNOW = 'LIGHT_SNOW'
    SNOW = 'SNOW'
    CONFIG = (
        ('1', FINE, '晴'),
        ('2', CLOUDY, '曇'),
        ('3', DRIZZLE, '小雨'),
        ('4', RAINY, '雨'),
        ('5', LIGHT_SNOW, '小雪'),
        ('6', SNOW, '雪')
    )
