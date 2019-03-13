from django.db import IntegrityError

from jrdb.models import RacetrackCode, Race
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
        ['furlong_time', 'ハロンタイム', '18', '3', '999', '9', '3*18=54BYTE 先頭馬の１ハロン毎のタイム 0.1秒単位　※１'],
        ['cor_1_pos', '１コーナー', None, '64', 'X', '63', None],
        ['cor_2_pos', '２コーナー', None, '64', 'X', '127', None],
        ['cor_3_pos', '３コーナー', None, '64', 'X', '191', None],
        ['cor_4_pos', '４コーナー', None, '64', 'X', '255', None],
        ['pace_up_pos', 'ペースアップ位置', None, '2', '9', '319', '残りハロン数'],  # TODO: 意味不明
        ['track_bias_1C', 'トラックバイアス（１角）', None, '3', 'X', '321', '（内、中、外）'],
        ['track_bias_2C', 'トラックバイアス（２角）', None, '3', 'X', '324', '（内、中、外）'],
        ['track_bias_backstretch', 'トラックバイアス（向正）', None, '3', 'X', '327', '（内、中、外）'],
        ['track_bias_3C', 'トラックバイアス（３角）', None, '3', 'X', '330', '（内、中、外）'],
        ['track_bias_4C', 'トラックバイアス（４角）', None, '5', 'X', '333', '（最内、内、中、外、大外）'],
        ['track_bias_homestretch', 'トラックバイアス（直線）', None, '5', 'X', '338', '（最内、内、中、外、大外）'],
        ['comment', 'レースコメント', None, '500', 'X', '343', None],
        ['reserved', '予備', None, '8', 'X', '843', 'スペース'],
        ['newline', '改行', None, '2', 'X', '851', 'ＣＲ・ＬＦ'],
    ]

    def clean(self):
        df = self.df[['racetrack_code']]

        racetrack_codes = {code.key: code.id for code in RacetrackCode.objects.filter(key__in=df.racetrack_code)}
        df['racetrack_id'] = df.racetrack_code.map(racetrack_codes).astype(int)
        df.drop(columns=['racetrack_code'], inplace=True)

        df['yr'] = self.df.yr.astype(int)
        df['round'] = self.df['round'].astype(int)
        df['day'] = self.df.day.astype(int)
        df['num'] = self.df.num.astype(int)

        df['track_bias_1C'] = self.df.track_bias_1C.apply(parse_comma_separated_integer_list, args=(1,))
        df['track_bias_2C'] = self.df.track_bias_2C.apply(parse_comma_separated_integer_list, args=(1,))
        df['track_bias_3C'] = self.df.track_bias_3C.apply(parse_comma_separated_integer_list, args=(1,))
        df['track_bias_4C'] = self.df.track_bias_4C.apply(parse_comma_separated_integer_list, args=(1,))
        df['track_bias_bs'] = self.df.track_bias_backstretch.apply(parse_comma_separated_integer_list, args=(1,))
        df['track_bias_hs'] = self.df.track_bias_homestretch.apply(parse_comma_separated_integer_list, args=(1,))

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
