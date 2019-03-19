from django.db import IntegrityError
import numpy as np

from jrdb.models.choices import AREA, TRAINEE_CATEGORY
from jrdb.models.jockey import Jockey
from jrdb.templates.parse import filter_na, parse_comma_separated_integer_list, parse_int_or, parse_date
from jrdb.templates.template import Template


class KZA(Template):
    """
    http://www.jrdb.com/program/Ks/Ks_doc1.txt
    """
    name = '全騎手'
    items = [
        ['code', '騎手コード', None, '5', '99999', '1', None],
        ['is_retired', '登録抹消フラグ', None, '1', '9', '6', '1:抹消,0:現役'],
        ['retired_on', '登録抹消年月日', None, '8', '9', '7', 'YYYYMMDD'],
        ['name', '騎手名', None, '12', 'X', '15', '全角６文字'],
        ['name_kana', '騎手カナ', None, '30', 'X', '27', '全角１５文字'],
        ['name_abbr', '騎手名略称', None, '6', 'X', '57', '全角３文字'],
        ['area', '所属コード', None, '1', '9', '63', '1:関東,2:関西,3:他'],
        ['training_center_name', '所属地域名', None, '4', 'X', '64', '全角２文字、地方の場合'],
        ['birthday', '生年月日', None, '8', '9', '68', 'YYYYMMDD'],
        ['lic_acquired_yr', '初免許年', None, '4', '9', '76', 'YYYY'],
        ['trainee_cat', '見習い区分', None, '1', '9', '80', '1:☆(1K減),2:△(2K),3:▲(3K)'],
        ['trainer_code', '所属厩舎', None, '5', '9', '81', '所属厩舎の調教師コード'],
        ['jrdb_comment', '騎手コメント', None, '40', 'X', '86', 'ＪＲＤＢスタッフの騎手評価'],
        ['jrdb_comment_date', 'コメント入力年月日', None, '8', 'X', '126', '騎手コメントを入力した年月日'],
        ['cur_yr_leading', '本年リーディング', None, '3', 'ZZ9', '134', None],
        ['cur_yr_flat_r', '本年平地成績', None, '12', 'ZZ9*4', '137', '１－２－３－着外(3*4)'],
        ['cur_yr_obst_r', '本年障害成績', None, '12', 'ZZ9*4', '149', '１－２－３－着外(3*4)'],
        ['cur_yr_sp_wins', '本年特別勝数', None, '3', 'ZZ9', '161', None],
        ['cur_yr_hs_wins', '本年重賞勝数', None, '3', 'ZZ9', '164', None],
        ['prev_yr_leading', '昨年リーディング', None, '3', 'ZZ9', '167', None],
        ['prev_yr_flat_r', '昨年平地成績', None, '12', 'ZZ9*4', '170', '１－２－３－着外(3*4)'],
        ['prev_yr_obst_r', '昨年障害成績', None, '12', 'ZZ9*4', '182', '１－２－３－着外(3*4)'],
        ['prev_yr_sp_wins', '昨年特別勝数', None, '3', 'ZZ9', '194', None],
        ['prev_yr_hs_wins', '昨年重賞勝数', None, '3', 'ZZ9', '197', None],
        ['sum_flat_r', '通算平地成績', None, '20', 'ZZZZ9*4', '200', '１－２－３－着外(5*4)'],
        ['sum_obst_r', '通算障害成績', None, '20', 'ZZZZ9*4', '220', '１－２－３－着外(5*4)'],
        ['saved_on', 'データ年月日', None, '8', 'X', '240', 'スペース'],
        ['reserved', '予備', None, '23', 'X', '248', 'スペース'],
        ['newline', '改行', None, '2', 'X', '271', 'ＣＲ・ＬＦ']
    ]

    def clean(self):
        retired_on = self.df.retired_on.apply(parse_date, args=('%Y%m%d',))
        retired_on.name = 'retired_on'

        df = retired_on.to_frame()
        df['name'] = self.df.name.str.strip()
        df['name_kana'] = self.df.name_kana.str.strip()
        df['name_abbr'] = self.df.name_abbr.str.strip()

        df['area'] = self.df.area.map(AREA.get_key_map())
        df['training_center_name'] = self.df.training_center_name.str.strip()
        df['birthday'] = self.df.birthday.apply(parse_date, args=('%Y%m%d',))
        df['lic_acquired_yr'] = self.df.lic_acquired_yr.astype(int)
        df['trainee_cat'] = self.df.trainee_cat.map(TRAINEE_CATEGORY.get_key_map())
        df['trainer_code'] = self.df.trainer_code.str.strip()
        df['jrdb_comment'] = self.df.jrdb_comment.str.strip()
        df['jrdb_comment_date'] = self.df.jrdb_comment_date.apply(parse_date, args=('%Y%m%d',))

        df['cur_yr_leading'] = self.df.cur_yr_leading.str.strip().apply(parse_int_or, args=(np.nan,)).astype('Int64')
        df['cur_yr_flat_r'] = self.df.cur_yr_flat_r.apply(parse_comma_separated_integer_list, args=(3,))
        df['cur_yr_obst_r'] = self.df.cur_yr_obst_r.apply(parse_comma_separated_integer_list, args=(3,))
        df['cur_yr_sp_wins'] = self.df.cur_yr_sp_wins.str.strip().apply(parse_int_or, args=(0,)).astype(int)
        df['cur_yr_hs_wins'] = self.df.cur_yr_hs_wins.str.strip().apply(parse_int_or, args=(0,)).astype(int)

        df['prev_yr_leading'] = self.df.prev_yr_leading.str.strip().apply(parse_int_or, args=(np.nan,)).astype('Int64')
        df['prev_yr_flat_r'] = self.df.prev_yr_flat_r.apply(parse_comma_separated_integer_list, args=(3,))
        df['prev_yr_obst_r'] = self.df.prev_yr_obst_r.apply(parse_comma_separated_integer_list, args=(3,))
        df['prev_yr_sp_wins'] = self.df.prev_yr_sp_wins.str.strip().apply(parse_int_or, args=(0,)).astype(int)
        df['prev_yr_hs_wins'] = self.df.prev_yr_hs_wins.str.strip().apply(parse_int_or, args=(0,)).astype(int)

        df['sum_flat_r'] = self.df.sum_flat_r.apply(parse_comma_separated_integer_list, args=(5,))
        df['sum_obst_r'] = self.df.sum_obst_r.apply(parse_comma_separated_integer_list, args=(5,))

        return df

    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            obj = filter_na(row)
            try:
                Jockey.objects.create(**obj)
            except IntegrityError:
                Jockey.objects.filter(code=obj['code']).update(**obj)
