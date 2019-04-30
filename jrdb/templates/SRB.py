import logging

from .item import ForeignKeyItem, IntegerItem, StringItem, ArrayItem
from .template import Template, ProgramRaceLoadMixin

logger = logging.getLogger(__name__)


class SRB(Template, ProgramRaceLoadMixin):
    """
    http://www.jrdb.com/program/Srb/srb_doc.txt
    """
    name = 'JRDB成績レースデータ（SRB）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),

        # TODO:
        #   - ArrayItem('ハロンタイム', 3, 8, 'furlong_time'),
        #   - ArrayItem('１コーナー', 64, 62, 'c1pos'),
        #   - ArrayItem('２コーナー', 64, 126, 'c2pos'),
        #   - ArrayItem('３コーナー', 64, 190, 'c3pos'),
        #   - ArrayItem('４コーナー', 64, 254, 'c4pos'),
        #   - ArrayItem('ペースアップ位置', 2, 318, 'pace_up_pos'),

        ArrayItem('トラックバイアス（１角）', 3, 320, 'jrdb.Race.c1_track_bias', 3),
        ArrayItem('トラックバイアス（２角）', 3, 323, 'jrdb.Race.c2_track_bias', 3),
        ArrayItem('トラックバイアス（向正）', 3, 326, 'jrdb.Race.bs_track_bias', 3),
        ArrayItem('トラックバイアス（３角）', 3, 329, 'jrdb.Race.c3_track_bias', 3),
        ArrayItem('トラックバイアス（４角）', 5, 332, 'jrdb.Race.c4_track_bias', 5),
        ArrayItem('トラックバイアス（直線）', 5, 337, 'jrdb.Race.hs_track_bias', 5),
        StringItem('レースコメント', 500, 342, 'jrdb.Race.comment'),
    ]
