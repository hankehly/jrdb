class ChoiceMixin:
    MAP = ()

    @classmethod
    def CHOICES(self):
        return (
            (t[1], t[2]) for t in self.MAP
        )

    @classmethod
    def get_key_map(cls):
        """
        Deprecated. Use options instead.
        """
        return cls.options()

    @classmethod
    def options(cls) -> dict:
        return {
            t[0]: t[1] for t in cls.MAP
        }


class AREA(ChoiceMixin):
    KANTOU = 'KANTOU'
    KANSAI = 'KANSAI'
    OTHER = 'OTHER'
    MAP = (
        ('1', KANTOU, '関東'),
        ('2', KANSAI, '関西'),
        ('3', OTHER, '他'),
    )


class APTITUDE_CODE(ChoiceMixin):
    """
    適性を３段階評価したもの。

    1 ◎ 得意
    2 ○ 普通
    3 △ 苦手
    """
    STRONG = 'STRONG'
    NORMAL = 'NORMAL'
    WEAK = 'WEAK'
    MAP = (
        ('1', STRONG, '得意'),
        ('2', NORMAL, '普通'),
        ('3', WEAK, '苦手'),
    )


class BLINKER(ChoiceMixin):
    """
    1 初装着
    2 再装着 => using again after having removed
    3 ブリンカ => using and not first time
    """
    FIRST_TIME_USE = 'FIRST_TIME_USE'
    RETRY = 'RETRY'
    USING = 'USING'
    MAP = (
        ('1', FIRST_TIME_USE, '初装着'),
        ('2', RETRY, '再装着'),
        ('3', USING, 'ブリンカ')
    )


class GRADE(ChoiceMixin):
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
    MAP = (
        ('1', G1, 'Ｇ１'),
        ('2', G2, 'Ｇ２'),
        ('3', G3, 'Ｇ３'),
        ('4', HIGH_STAKES, '重賞'),
        ('5', SPECIAL, '特別'),
        ('6', LISTED, 'Ｌ（リステッド競走）')
    )


class COURSE_LABEL(ChoiceMixin):
    A = 'A'
    A1 = 'A1'
    A2 = 'A2'
    B = 'B'
    C = 'C'
    D = 'D'
    MAP = (
        ('1', A, 'A'),
        ('2', A1, 'A1'),
        ('3', A2, 'A2'),
        ('4', B, 'B'),
        ('5', C, 'C'),
        ('6', D, 'D'),
    )


class COURSE_INOUT(ChoiceMixin):
    INSIDE = 'INSIDE'
    OUTSIDE = 'OUTSIDE'
    STRAIGHT_DIRT = 'STRAIGHT_DIRT'
    OTHER = 'OTHER'
    MAP = (
        ('1', INSIDE, '通常(内)'),
        ('2', OUTSIDE, '外'),
        ('3', STRAIGHT_DIRT, '直ダ'),
        ('9', OTHER, '他'),
    )


class DEMEANOR(ChoiceMixin):
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
    MAP = (
        ('1', GOOD_CONDITION, '状態良'),
        ('2', NORMAL, '平凡'),
        ('3', UNSTABLE, '不安定'),
        ('4', EXCITED, 'イレ込'),
        ('5', GOOD_SPIRIT, '気合良'),
        ('6', LACKING_SPIRIT, '気不足'),
        ('7', RESTLESS, 'チャカ'),
        ('8', EXCITED_AND_RESTLESS, 'イレチ（イレ込+チャカつき）')
    )


class DIRECTION(ChoiceMixin):
    RIGHT = 'RIGHT'
    LEFT = 'LEFT'
    STRAIGHT = 'STRAIGHT'
    OTHER = 'OTHER'
    MAP = (
        ('1', RIGHT, '右'),
        ('2', LEFT, '左'),
        ('3', STRAIGHT, '直'),
        ('4', OTHER, '他')
    )


class FIGURE_OVERALL(ChoiceMixin):
    """
    体型

    1:長方形
    2:普通
    3:正方形
    """
    RECT = 'RECT'
    NORMAL = 'NORMAL'
    SQUARE = 'SQUARE'
    MAP = (
        ('1', RECT, '長方形'),
        ('2', NORMAL, '普通'),
        ('3', SQUARE, '正方形'),
    )


class FIGURE_SIZE(ChoiceMixin):
    """
    大きさ

    1:大きい
    2:普通
    3:小さい
    """
    LARGE = 'LARGE'
    NORMAL = 'NORMAL'
    SMALL = 'SMALL'
    MAP = (
        ('1', LARGE, '大きい'),
        ('2', NORMAL, '普通'),
        ('3', SMALL, '小さい'),
    )


class FIGURE_ANGLE(FIGURE_SIZE):
    """
    角度

    1:大きい
    2:普通
    3:小さい

    (same values as FIGURE_SIZE)
    """
    pass


class FIGURE_STRIDE(ChoiceMixin):
    """
    歩幅

    1:広い
    2:普通
    3:狭い
    """
    WIDE = 'WIDE'
    NORMAL = 'NORMAL'
    NARROW = 'NARROW'
    MAP = (
        ('1', WIDE, '広い'),
        ('2', NORMAL, '普通'),
        ('3', NARROW, '狭い'),
    )


class FIGURE_LENGTH(ChoiceMixin):
    """
    長さ

    1:長い
    2:普通
    3:短い
    """
    LONG = 'LONG'
    NORMAL = 'NORMAL'
    SHORT = 'SHORT'
    MAP = (
        ('1', LONG, '長い'),
        ('2', NORMAL, '普通'),
        ('3', SHORT, '短い'),
    )


class FLAT_OUT_RUN_TYPE(ChoiceMixin):
    """
    激走タイプ

    激走馬選定の候補に上がった馬を含めた、激走馬のタイプです。
    穴馬分析用データとして出力しました。

    タイプ
    A1 激走馬、中位人気グループで激走指数１番手
    A2 激走馬、中位人気グループで激走指数２番手
    A3 激走馬、中位人気グループで激走指数３番手
    A4 中位人気グループで激走指数４番手
    B1 下位人気グループで激走指数１番手
    B2 下位人気グループで激走指数１番手

    基本的によく来ている激走馬は、"A1"と"A2"です。
    現在"A4","B1","B2"は、激走馬としていません。

    ※以前は、３頭目の激走馬は"B1"にしていましたが、成績が良くないため、"A3"に変更しました。
    激走馬は分析により、最適な激走馬タイプに変更される可能性があります。
    過去分析される場合は、激走タイプを使用することをお勧めします。
    """
    A1 = 'A1'
    A2 = 'A2'
    A3 = 'A3'
    A4 = 'A4'
    B1 = 'B1'
    B2 = 'B2'
    MAP = (
        ('A1', A1, '激走馬、中位人気グループで激走指数１番手'),
        ('A2', A2, '激走馬、中位人気グループで激走指数２番手'),
        ('A3', A3, '激走馬、中位人気グループで激走指数３番手'),
        ('A4', A4, '中位人気グループで激走指数４番手'),
        ('B1', B1, '下位人気グループで激走指数１番手'),
        ('B2', B2, '下位人気グループで激走指数１番手')
    )


class PASTURE_RANK(ChoiceMixin):
    """
    放牧先ランク

    休み明けの放牧先データを分析して放牧先ランクを作成。

    連対率を放牧先別に分析し、ランク分けを行いました。
    １３％以上　　Ａランク　「休み明けのハンデが無い」ということ
    １１－１３％　Ｂランク
    ９－１１％　　Ｃランク　普通
    ７－９％　　　Ｄランク
    ７％以下　　　Ｅランク

    ※データが２０件以下はランク未設定としています。

    ※入厩・放牧先データについての注意事項
    ・放牧先に関して「○○県」「○○町」など、地域のみ掲載する場合があります。
    ・入厩のパターン等によっては、入厩データがない場合もあります。
    ・入厩情報に関してはレース前日にＪＲＤＢが入手しているデータまでが反映されます。
    ・入厩データが出走に間に合っていない場合、また入厩データがない場合は「情報無し」となります。
    ・間に合わなかったデータは後日取り込まれることになります。それを反映したデータは定期的に再作成
    します。
    """
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    MAP = (
        ('A', A, 'Ａランク (休み明けのハンデが無い)'),
        ('B', B, 'Ｂランク'),
        ('C', C, 'Ｃランク (普通)'),
        ('D', D, 'Ｄランク'),
        ('E', E, 'Ｅランク'),
    )


class PHYSIQUE(ChoiceMixin):
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
    MAP = (
        ('1', FAT, '太い'),
        ('2', OVERWEIGHT, '余裕'),
        ('3', GOOD, '良い'),
        ('4', NORMAL, '普通'),
        ('5', THIN, '細い'),
        ('6', FRESH, '張り'),
        ('7', LOOSE, '緩い')
    )


class PRIOR_CONTEXT_RACE_CLASS(ChoiceMixin):
    NO_CHANGE = 'NO_CHANGE'
    POST_PROMOTION_FIRST = 'POST_PROMOTION_FIRST'
    RANK_LOWERED = 'RANK_LOWERED'
    ATTEMPT_RISE_RANK = 'ATTEMPT_RISE_RANK'


class PRIOR_CONTEXT_SURFACE(ChoiceMixin):
    NO_CHANGE = 'NO_CHANGE'
    CHANGE = 'CHANGE'
    FIRST = 'FIRST'


class HORSE_SYMBOL(ChoiceMixin):
    """
    馬記号コード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    MAP = (
        ('01', '01', '○抽'),
        ('02', '02', '□抽'),
        ('03', '03', '○父'),
        ('04', '04', '○市'),
        ('05', '05', '○地'),
        ('06', '06', '○外'),
        ('07', '07', '○父○抽'),
        ('08', '08', '○父○市'),
        ('09', '09', '○父○地'),
        ('10', '10', '○市○地'),
        ('11', '11', '○外○地'),
        ('12', '12', '○父○市○地'),
        ('15', '15', '○招'),
        ('16', '16', '○招○外'),
        ('17', '17', '○招○父'),
        ('18', '18', '○招○市'),
        ('19', '19', '○招○父○市'),
        ('20', '20', '○父○外'),
        ('21', '21', '□地'),
        ('22', '22', '○外□地'),
        ('23', '23', '○父□地'),
        ('24', '24', '○市□地'),
        ('25', '25', '○父○市□地'),
        ('26', '26', '□外'),
        ('27', '27', '○父□外')
    )


class HOST_CATEGORY(ChoiceMixin):
    """
    開催区分

    1:関東
    2:関西
    3:ローカル
    """
    KANTOU = 'KANTOU'
    KANSAI = 'KANSAI'
    LOCAL = 'LOCAL'
    MAP = (
        ('1', KANTOU, '関東'),
        ('2', KANSAI, '関西'),
        ('3', LOCAL, 'ローカル'),
    )


class IMPOST_CLASS(ChoiceMixin):
    """
    重量

    http://www.jrdb.com/program/jrdb_code.txt
    http://cattle.x-winz.net/edb2_manual/12-3-99-CODE.html#C2008
    """
    HANDICAP = 'HANDICAP'
    SPECIAL_WEIGHT = 'SPECIAL_WEIGHT'
    WEIGHT_FOR_AGE = 'WEIGHT_FOR_AGE'
    SPECIAL_WEIGHT_AGE_SEX = 'SPECIAL_WEIGHT_AGE_SEX'
    MAP = (
        ('1', HANDICAP, 'ハンデ'),
        ('2', SPECIAL_WEIGHT, '別定'),
        ('3', WEIGHT_FOR_AGE, '馬齢'),
        ('4', SPECIAL_WEIGHT_AGE_SEX, '定量')
    )


class IMPROVEMENT(ChoiceMixin):
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
    MAP = (
        ('1', AA, 'AA'),
        ('2', A, 'A'),
        ('3', B, 'B'),
        ('4', C, 'C'),
        ('5', Q, '?')
    )


class PADDOCK_OBSERVED_HOOF(ChoiceMixin):
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
    MAP = (
        ('01', '01', '大ベタ'),
        ('02', '02', '中ベタ'),
        ('03', '03', '小ベタ'),
        ('04', '04', '細ベタ'),
        ('05', '05', '大立'),
        ('06', '06', '中立'),
        ('07', '07', '小立'),
        ('08', '08', '細立'),
        ('09', '09', '大標準'),
        ('10', '10', '中標準'),
        ('11', '11', '小標準'),
        ('12', '12', '細標準'),
        ('17', '17', '大標起'),
        ('18', '18', '中標起'),
        ('19', '19', '小標起'),
        ('20', '20', '細標起'),
        ('21', '21', '大標ベ'),
        ('22', '22', '中標ベ'),
        ('23', '23', '小標ベ'),
        ('24', '24', '細標ベ')
    )


class PENALTY(ChoiceMixin):
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
    MAP = (
        ('0', NORMAL, '異常なし'),
        ('1', SCRATCHED, '取消'),
        ('2', EXCLUDED, '除外'),
        ('3', FAIL_TO_FINISH, '中止'),
        ('4', DISQUALIFIED, '失格'),
        ('5', DISQUALIFIED_AND_PLACED, '降着'),
        ('6', REMOUNT, '再騎乗')
    )


class PACE_CATEGORY(ChoiceMixin):
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    SLOW = 'SLOW'
    MAP = (
        ('H', HIGH, 'ハイ'),
        ('M', MEDIUM, '平均'),
        ('S', SLOW, 'スロー')
    )


class RACE_CATEGORY(ChoiceMixin):
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
    MAP = (
        ('11', TWO_YR_OLD, '2歳'),
        ('12', THREE_YR_OLD, '3歳'),
        ('13', THREE_YR_OLD_AND_UP, '3歳以上'),
        ('14', FOUR_YR_OLD_AND_UP, '4歳以上'),
        ('20', OBSTACLE, '障害'),
        ('99', OTHER, 'その他')
    )


class RACE_DEVELOPMENT_SYMBOL(ChoiceMixin):
    """
    展開記号コード

      記号  内容
    1 "<"   逃馬
    2 "@"   上がりの最も速い馬
    3 "*"   上がりの速い馬(2,3番目)
    4 "?"   データ不足で確認が必要な馬
    0 "("   その他
    """
    FRONT_RUNNER = 'FRONT_RUNNER'
    FASTEST_F3F = 'FASTEST_F3F'
    FAST_F3F = 'FAST_F3F'
    LACK_DATA = 'LACK_DATA'
    OTHER = 'OTHER'
    MAP = (
        ('1', FRONT_RUNNER, '逃馬'),
        ('2', FASTEST_F3F, '上がりの最も速い馬'),
        ('3', FAST_F3F, '上がりの速い馬(2,3番目)'),
        ('4', LACK_DATA, 'データ不足で確認が必要な馬'),
        ('0', OTHER, 'その他')
    )


class RACE_LINE(ChoiceMixin):
    """
    コース取り

    https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1373948028
    """
    INNERMOST = 'INNERMOST'
    INNER = 'INNER'
    MIDDLE = 'MIDDLE'
    OUTER = 'OUTER'
    OUTERMOST = 'OUTERMOST'
    MAP = (
        ('1', INNERMOST, '最内'),
        ('2', INNER, '内'),
        ('3', MIDDLE, '中'),
        ('4', OUTER, '外'),
        ('5', OUTERMOST, '大外')
    )


class RACE_HORSE_SEX_SYMBOL(ChoiceMixin):
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
    MAP = (
        ('0', NA, 'なし'),
        ('1', MALE, '牡馬限定'),
        ('2', FEMALE, '牝馬限定'),
        ('3', MALE_CASTRATED, '牡・せん馬限定'),
        ('4', FEMALE_CASTRATED, '牡・牝馬限定')
    )


class RACE_HORSE_TYPE_SYMBOL(ChoiceMixin):
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
    MAP = (
        ('0', NA, 'なし'),
        ('1', MIX, '○混'),
        ('2', D, '○父'),
        ('3', A_S, '○市○抽'),
        ('4', KYU, '九州産限定'),
        ('5', INT, '○国際混')
    )


class RACE_INTERLEAGUE_SYMBOL(ChoiceMixin):
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
    MAP = (
        ('0', NA, 'なし'),
        ('1', DSN, '○指'),
        ('2', DES, '□指'),
        ('3', SD, '○特指'),
        ('4', JUNIOR, '若手')
    )


class RANK_LOWERED(ChoiceMixin):
    """
    1 降級
    2 ２段階降級
    0 通常
    """
    SINGLE = 'SINGLE'
    DOUBLE = 'DOUBLE'
    NO_CHANGE = 'NO_CHANGE'
    MAP = (
        ('1', SINGLE, '降級'),
        ('2', DOUBLE, '２段階降級'),
        ('0', NO_CHANGE, '通常')
    )


class REST_REASON(ChoiceMixin):
    """
    休養理由分類コード

    http://www.jrdb.com/program/jrdb_code.txt
    """
    MAP = (
        ('01', '01', '放牧'),
        ('02', '02', '放牧(故障、骨折等)'),
        ('03', '03', '放牧(不安、ソエ等)'),
        ('04', '04', '放牧(病気)'),
        ('05', '05', '放牧(再審査)'),
        ('06', '06', '放牧(出走停止)'),
        ('07', '07', '放牧(手術）'),
        ('11', '11', '調整'),
        ('12', '12', '調整(故障、骨折等)'),
        ('13', '13', '調整(不安、ソエ等)'),
        ('14', '14', '調整(病気)')
    )


class RUNNING_STYLE(ChoiceMixin):
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
    MAP = (
        ('1', FRONT_RUNNER, '逃げ'),
        ('2', STALKER, '先行'),
        ('3', OTP, '差し'),
        ('4', OTP_STRETCH, '追込'),
        ('5', OTP_GOOD_POS, '好位差し'),
        ('6', VERSATILE, '自在')
    )


class SEX(ChoiceMixin):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    CASTRATED = 'CASTRATED'
    MAP = (
        ('1', MALE, 'Male'),
        ('2', FEMALE, 'Female'),
        ('3', CASTRATED, 'Castrated')
    )


class STABLE_HORSE_EVALUATION(ChoiceMixin):
    """
    厩舎評価コード

    厩舎サイドの期待度をわかりやすく４段階評価したもの。
    1 超強気
    2 強気
    3 現状維持
    4 弱気

    http://www.jrdb.com/program/jrdb_code.txt
    """
    SUPER_CONFIDENT = 'SUPER_CONFIDENT'
    CONFIDENT = 'CONFIDENT'
    NO_CHANGE = 'NO_CHANGE'
    NOT_CONFIDENT = 'NOT_CONFIDENT'
    MAP = (
        ('1', SUPER_CONFIDENT, '超強気'),
        ('2', CONFIDENT, '強気'),
        ('3', NO_CHANGE, '現状維持'),
        ('3', NOT_CONFIDENT, '弱気'),
    )


class STABLE_RANK(ChoiceMixin):
    S = 'S'
    A = 'A'
    B = 'B'
    NORMAL = 'NORMAL'
    D = 'D'
    E = 'E'
    F = 'F'
    BELOW_F = 'BELOW_F'

    MAP = (
        ('1', S, 'S級 ピンク'),
        ('2', A, 'A級 オレンジ'),
        ('3', B, 'B級 黄色'),
        ('5', NORMAL, 'ノーマル'),
        ('6', D, 'D級 青'),
        ('7', E, 'E級 紫'),
        ('8', F, 'F級 灰色'),
        ('9', BELOW_F, 'その他総数１０以下の厩舎')
    )


class SURFACE(ChoiceMixin):
    TURF = 'TURF'
    DIRT = 'DIRT'
    OBSTACLE = 'OBSTACLE'
    MAP = (
        ('1', TURF, '芝'),
        ('2', DIRT, 'ダート'),
        ('3', OBSTACLE, '障害'),
    )


class TAIL_SWING_INTENSITY(ChoiceMixin):
    """
    尾の振り方

    1:激しい
    2:少し
    3:あまり振らない
    """
    HIGH = 'HIGH'
    LOW = 'LOW'
    BARELY = 'BARELY'


class TRAINING_RESULT_IDX_CHANGE(ChoiceMixin):
    """
    仕上指数変化（参考値）

    前走（中央競馬のレース出走時）の仕上指数との比較です。
    1 ++(攻め強化大)
    2 + (攻め強化)
    3   (平行線)
    4 - (攻め弱化)
    """
    BOLSTER_MAX = 'BOLSTER_MAX'
    BOLSTER = 'BOLSTER'
    NO_CHANGE = 'NO_CHANGE'
    WEAKEN = 'WEAKEN'
    MAP = (
        ('1', BOLSTER_MAX, '++(攻め強化大)'),
        ('2', BOLSTER, '+ (攻め強化)'),
        ('3', NO_CHANGE, '(平行線)'),
        ('4', WEAKEN, '- (攻め弱化)')
    )


class TRAINING_AMOUNT_EVAL(ChoiceMixin):
    """
    調教量評価
    調教量についての評価です。

    A （多い）
    B （普通）
    C （少ない）
    D （非常に少ない）
    """
    LARGE = 'LARGE'
    NORMAL = 'NORMAL'
    SMALL = 'SMALL'
    VERY_LITTLE = 'VERY_LITTLE'
    MAP = (
        ('A', LARGE, '多い'),
        ('B', NORMAL, '普通'),
        ('C', SMALL, '少ない'),
        ('D', VERY_LITTLE, '非常に少ない'),
    )


class THREE_STAGE_EVAL(ChoiceMixin):
    """
    ３段階評価

    1 ◎
    2 ○
    3 △
    """
    BEST = 'BEST'
    GOOD = 'GOOD'
    OK = 'OK'
    MAP = (
        ('1', BEST, '◎'),
        ('2', GOOD, '○'),
        ('3', OK, '△'),
    )


class TRACK_CONDITION(ChoiceMixin):
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
    MAP = (
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


class TRACK_CONDITION_KA(ChoiceMixin):
    """
    内|中|外などの馬場状態(KABのみで使用)

    1: 絶好
    2: 良
    3: 稍荒
    4: 荒
    """
    GREAT = 'GREAT'
    GOOD = 'GOOD'
    SLIGHT_ROUGH = 'SLIGHT_ROUGH'
    ROUGH = 'ROUGH'
    MAP = (
        ('1', GREAT, '絶好'),
        ('2', GOOD, '良'),
        ('3', SLIGHT_ROUGH, '稍荒'),
        ('4', ROUGH, '荒')
    )


class TRAINING_COURSE_CATEGORY(ChoiceMixin):
    """
    調教コース種別
    調教コースは、トラックを周回する「コース調教」と、「坂路調教」に大別されます。
    ここでは、中間での主な調教コースを示します。

    http://www.jrdb.com/program/Cyb/cybsiyo_doc.txt
    """
    MAP = (
        ('1', '1', '坂路調教'),
        ('2', '2', 'コース調教'),
        ('3', '3', '併用(坂路、コース併用)'),
        ('4', '4', '障害（障害練習）'),
        ('5', '5', '障害他（障害練習＋α）'),
        ('0', '0', '他（調教なし、不明）')
    )


class TRAINING_DISTANCE(ChoiceMixin):
    """
    調教距離

    本追い切り（※）の調教距離です。
    1 長め
    2 標準
    3 短め
    4 ２本
    0 他（調教なし、不明）

    ※【本追い切り】の定義
    基本的にレース週の水曜、木曜の調教で1番強い調教を【本追い切り】としています。
    """
    LONG = 'LONG'
    NORMAL = 'NORMAL'
    SHORT = 'SHORT'
    TWO_RUNS = 'TWO_RUNS'
    OTHER = 'OTHER'
    MAP = (
        ('1', LONG, '長め'),
        ('2', NORMAL, '標準'),
        ('3', SHORT, '短め'),
        ('4', TWO_RUNS, '２本'),
        ('0', OTHER, '他（調教なし、不明）'),
    )


class TRAINING_EMPHASIS(ChoiceMixin):
    """
    調教重点

    本追い切りにおいて"テン"、"中間"、"終い"のどの部分に重点を置いたかを調教時計から分析しています。

    1 テン重点
    2 中間重点
    3 終い重点
    4 平均的
    0 他（調教なし、不明）
    """
    F3F = 'F3F'
    MID = 'MID'
    L3F = 'L3F'
    AVG = 'AVG'
    OTHER = 'OTHER'
    MAP = (
        ('1', F3F, 'テン重点'),
        ('2', MID, '中間重点'),
        ('3', L3F, '終い重点'),
        ('4', AVG, '平均的'),
        ('0', OTHER, '他（調教なし、不明）'),
    )


class TRAINING_STYLE(ChoiceMixin):
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
    MAP = (
        ('01', '01', 'スパルタ'),
        ('02', '02', '標準多め'),
        ('03', '03', '乗込'),
        ('04', '04', '一杯平均'),
        ('05', '05', '標準'),
        ('06', '06', '馬ナリ平均'),
        ('07', '07', '急仕上げ'),
        ('08', '08', '標準少め'),
        ('09', '09', '軽目'),
        ('10', '10', '連闘'),
        ('11', '11', '調教なし')
    )


class TRAINER_HORSE_EVALUATION(ChoiceMixin):
    """
    調教矢印コード
    調教から見た馬の調子をわかりやすく５段階評価したもの。
    1 デキ抜群
    2 上昇
    3 平行線
    4 やや下降気味
    5 デキ落ち
    """
    OUTSTANDING = 'OUTSTANDING'
    IMPROVING = 'IMPROVING'
    NO_CHANGE = 'NO_CHANGE'
    DOWNWARD_TREND = 'DOWNWARD_TREND'
    POOR = 'POOR'
    MAP = (
        ('1', OUTSTANDING, 'デキ抜群'),
        ('2', IMPROVING, '上昇'),
        ('3', NO_CHANGE, '平行線'),
        ('4', DOWNWARD_TREND, 'やや下降気味'),
        ('5', POOR, 'デキ落ち')
    )


class TRANSPORT_CATEGORY(ChoiceMixin):
    """
    輸送区分
    滞在、遠征などの輸送過程を表します。直前輸送（直輸）を通常／遠征に分けました。
    1 滞在 ローカル競馬場で、競馬場に入厩している馬を表します。
    2 通常 栗東→京都、美浦→中山等や、札幌→函館を通常としています。
    3 遠征 栗東→中山、栗東→小倉等の長距離輸送を遠征としています。
    4 連闘 下記【滞在】の説明参照
    0 不明

    輸送区分は、レース週の最終追い切り（通常は、水or木）の場所で判断しています。

    【滞在】の定義
    　ローカル競馬場（札幌、函館、福島、新潟、小倉）開催において
    　レース週の最終追い切りを、当該競馬場で行っている場合、【滞在】としています。
    　連闘馬の場合、おそらく滞在と思われますが、"連闘"と分類しています。
    　滞在馬で分析する場合、"滞在" あるいは"連闘"と指定すると実際的です。

    http://www.jrdb.com/program/Kyi/ky_siyo_doc.txt
    """
    STAY = 'STAY'
    NORMAL = 'NORMAL'
    VISIT = 'VISIT'
    UNKNOWN = 'UNKNOWN'

    MAP = (
        ('1', STAY, '滞在'),
        ('2', NORMAL, '通常'),
        ('3', VISIT, '遠征'),
        ('0', UNKNOWN, '不明'),
    )


class TURF_TYPE(ChoiceMixin):
    """
    芝種類

    https://keiba-thetop.com/shibamain/#outline__1_1
    """
    NATURAL = 'NATURAL'
    WESTERN = 'WESTERN'
    MIXED = 'MIXED'
    MAP = (
        ('1', NATURAL, '野芝'),
        ('2', WESTERN, '洋芝'),
        ('3', MIXED, '混生'),
    )


class HAIR_COLOR(ChoiceMixin):
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
    MAP = (
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


class WEATHER(ChoiceMixin):
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
    MAP = (
        ('1', FINE, '晴'),
        ('2', CLOUDY, '曇'),
        ('3', DRIZZLE, '小雨'),
        ('4', RAINY, '雨'),
        ('5', LIGHT_SNOW, '小雪'),
        ('6', SNOW, '雪')
    )


class WEIGHT_REDUCTION(ChoiceMixin):
    """
    1: (1K減) ☆
    2: (2K減) △
    3: (3K減) ▲

    http://www.jra.go.jp/kouza/yougo/w574.html
    """
    REDUCE_1K = 'REDUCE_1K'
    REDUCE_2K = 'REDUCE_2K'
    REDUCE_3K = 'REDUCE_3K'
    MAP = (
        ('1', REDUCE_1K, '1K減'),
        ('2', REDUCE_2K, '2K減'),
        ('3', REDUCE_3K, '3K減'),
    )


class YIELDING_TRACK_APTITUDE(APTITUDE_CODE):
    """
    重適性コード

    過去の成績、蹄の形状等よりその馬の重馬場への適性を３段階評価したもの。
    1 ◎ 得意
    2 ○ 普通
    3 △ 苦手
    """
    pass
