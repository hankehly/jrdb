from django.db import IntegrityError

from jrdb.models import Racetrack, Race
from jrdb.templates.parse import parse_comma_separated_integer_list, filter_na
from jrdb.templates.template import Template


class SRB(Template):
    """
    http://www.jrdb.com/program/Srb/srb_doc.txt
    """
    name = 'JRDB成績レースデータ（SRB）'
    items = [
        ['racetrack_code', '場コード', None, '2', '99', '1', None],
        ['yr', '年', None, '2', '99', '3', None],
        ['round', '回', None, '1', '9', '5', None],
        ['day', '日', None, '1', 'F', '6', None],
        ['num', 'Ｒ', None, '2', '99', '7', None],
        ['furlong_time', 'ハロンタイム', '18', '3', '999', '9', '3*18=54BYTE 先頭馬の１ハロン毎のタイム 0.1秒単位　※１'],  # IGNORED
        ['cor_1_pos', '１コーナー', None, '64', 'X', '63', None],  # IGNORED
        ['cor_2_pos', '２コーナー', None, '64', 'X', '127', None],  # IGNORED
        ['cor_3_pos', '３コーナー', None, '64', 'X', '191', None],  # IGNORED
        ['cor_4_pos', '４コーナー', None, '64', 'X', '255', None],  # IGNORED
        ['pace_up_pos', 'ペースアップ位置', None, '2', '9', '319', '残りハロン数'],  # IGNORED
        ['c1_track_bias', 'トラックバイアス（１角）', None, '3', 'X', '321', '（内、中、外）'],
        ['c2_track_bias', 'トラックバイアス（２角）', None, '3', 'X', '324', '（内、中、外）'],
        ['bs_track_bias', 'トラックバイアス（向正）', None, '3', 'X', '327', '（内、中、外）'],
        ['c3_track_bias', 'トラックバイアス（３角）', None, '3', 'X', '330', '（内、中、外）'],
        ['c4_track_bias', 'トラックバイアス（４角）', None, '5', 'X', '333', '（最内、内、中、外、大外）'],
        ['hs_track_bias', 'トラックバイアス（直線）', None, '5', 'X', '338', '（最内、内、中、外、大外）'],
        ['comment', 'レースコメント', None, '500', 'X', '343', None],
        ['reserved', '予備', None, '8', 'X', '843', 'スペース'],
        ['newline', '改行', None, '2', 'X', '851', 'ＣＲ・ＬＦ'],
    ]

    def clean(self):
        racetracks = Racetrack.objects.filter(code__in=self.df.racetrack_code).values('code', 'id')
        s = self.df.racetrack_code.map({racetrack['code']: racetrack['id'] for racetrack in racetracks})
        s.name = 'racetrack_id'

        df = s.to_frame()
        df['yr'] = self.df.yr.astype(int)
        df['round'] = self.df['round'].astype(int)
        df['day'] = self.df.day.astype(int)
        df['num'] = self.df.num.astype(int)

        df['c1_track_bias'] = self.df.c1_track_bias.apply(parse_comma_separated_integer_list, args=(1,))
        df['c2_track_bias'] = self.df.c2_track_bias.apply(parse_comma_separated_integer_list, args=(1,))
        df['c3_track_bias'] = self.df.c3_track_bias.apply(parse_comma_separated_integer_list, args=(1,))
        df['c4_track_bias'] = self.df.c4_track_bias.apply(parse_comma_separated_integer_list, args=(1,))
        df['bs_track_bias'] = self.df.bs_track_bias.apply(parse_comma_separated_integer_list, args=(1,))
        df['hs_track_bias'] = self.df.hs_track_bias.apply(parse_comma_separated_integer_list, args=(1,))

        df['comment'] = self.df.comment.str.strip()

        return df

    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            obj = filter_na(row)
            try:
                Race.objects.create(**obj)
            except IntegrityError:
                Race.objects.filter(
                    racetrack_id=obj['racetrack_id'],
                    yr=obj['yr'],
                    round=obj['round'],
                    day=obj['day'],
                    num=obj['num']
                ).update(**obj)
