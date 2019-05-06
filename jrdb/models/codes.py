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


class HoofCode(SimpleCode):
    """
    脚元コード

    http://www.jrdb.com/program/ashimoto_code.txt
    """
    value_abbr = models.CharField(max_length=255)

    class Meta:
        db_table = 'hoof_codes'


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


class PaceFlowCode(SimpleCode):
    """
    ［前３Ｆ］［その間］［後３Ｆ］のタイムを利用してペースの流れを視覚で捉えます。

    コード 表示 意味
    33     ＼   前半飛ばす
    22    ――    平均ペース
    11    ／    後半型
    32    ＼＿  テン飛ばす
    31    ＼／  なかだるみ
    23    ￣＼  テンから飛ばし失速
    21    ＿／  上がり速い
    13    ／＼  ペースアップが早く失速
    12    ／￣  ペースアップが早く持続
    """
    display = models.CharField(max_length=2)

    class Meta:
        db_table = 'pace_flow_codes'


class Pedigree(models.Model):
    objects = SimpleCodeManager()

    key = models.CharField(max_length=255, unique=True)
    strain_small = models.CharField(max_length=255)
    strain_large = models.CharField(max_length=255)


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


class SpecialMentionCode(SimpleCode):
    """
    特記コード

    http://www.jrdb.com/program/tokki_code.txt
    """

    class Meta:
        db_table = 'special_mention_codes'
