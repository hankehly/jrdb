import logging

from django.db import IntegrityError, transaction

from jrdb.models import Race
from jrdb.templates.parse import parse_comma_separated_integer_list, filter_na
from jrdb.templates.template import Template, Item

logger = logging.getLogger(__name__)


class SRB(Template):
    """
    http://www.jrdb.com/program/Srb/srb_doc.txt
    """
    name = 'JRDB成績レースデータ（SRB）'
    items = [
        Item('jrdb.Race.racetrack', '場コード', 2, 0),
        Item('jrdb.Race.yr', '年', 2, 2),
        Item('jrdb.Race.round', '回', 1, 4),
        Item('jrdb.Race.day', '日', 1, 5),
        Item('jrdb.Race.num', 'Ｒ', 2, 6),

        Item('furlong_time', 'ハロンタイム', 3, 8, repeat=18, notes='3*18=54BYTE 先頭馬の１ハロン毎のタイム 0.1秒単位　※１', use=False),
        Item('c1pos', '１コーナー', 64, 62, use=False),
        Item('c2pos', '２コーナー', 64, 126, use=False),
        Item('c3pos', '３コーナー', 64, 190, use=False),
        Item('c4pos', '４コーナー', 64, 254, use=False),
        Item('pace_up_pos', 'ペースアップ位置', 2, 318, notes='残りハロン数', use=False),

        Item('jrdb.Race.c1_track_bias', 'トラックバイアス（１角）', 3, 320, notes='（内、中、外）'),
        Item('jrdb.Race.c2_track_bias', 'トラックバイアス（２角）', 3, 323, notes='（内、中、外）'),
        Item('jrdb.Race.bs_track_bias', 'トラックバイアス（向正）', 3, 326, notes='（内、中、外）'),
        Item('jrdb.Race.c3_track_bias', 'トラックバイアス（３角）', 3, 329, notes='（内、中、外）'),
        Item('jrdb.Race.c4_track_bias', 'トラックバイアス（４角）', 5, 332, notes='（最内、内、中、外、大外）'),
        Item('jrdb.Race.hs_track_bias', 'トラックバイアス（直線）', 5, 337, notes='（最内、内、中、外、大外）'),
        Item('jrdb.Race.comment', 'レースコメント', 500, 342),

        Item('reserved', '予備', 8, 842, notes='スペース', use=False),
        Item('newline', '改行', 2, 850, notes='ＣＲ・ＬＦ', use=False),
    ]

    def clean_c1_track_bias(self):
        return self.df.c1_track_bias.apply(parse_comma_separated_integer_list, args=(1,))

    def clean_c2_track_bias(self):
        return self.df.c2_track_bias.apply(parse_comma_separated_integer_list, args=(1,))

    def clean_c3_track_bias(self):
        return self.df.c3_track_bias.apply(parse_comma_separated_integer_list, args=(1,))

    def clean_c4_track_bias(self):
        return self.df.c4_track_bias.apply(parse_comma_separated_integer_list, args=(1,))

    def clean_bs_track_bias(self):
        return self.df.bs_track_bias.apply(parse_comma_separated_integer_list, args=(1,))

    def clean_hs_track_bias(self):
        return self.df.hs_track_bias.apply(parse_comma_separated_integer_list, args=(1,))

    @transaction.atomic
    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            obj = filter_na(row)

            unique_key = {
                'racetrack_id': obj.pop('racetrack_id'),
                'yr': obj.pop('yr'),
                'round': obj.pop('round'),
                'day': obj.pop('day'),
                'num': obj.pop('num')
            }

            try:
                Race.objects.update_or_create(**unique_key, defaults=obj)
            except IntegrityError as e:
                logger.exception(e)
