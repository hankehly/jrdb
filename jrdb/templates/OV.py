import logging

from jrdb.templates.item import ArrayItem, IntegerItem, StringItem, ForeignKeyItem
from .OZ import OZ

logger = logging.getLogger(__name__)


class OV(OZ):
    """
    http://www.jrdb.com/program/Ov/ovdata_doc.txt
    """
    name = '３連単基準オッズデータ（OV）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Race.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Race.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Race.round'),
        StringItem('日', 1, 5, 'jrdb.Race.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('登録頭数', 2, 8, 'jrdb.Race.contender_count'),
        ArrayItem('３連単オッズ', 7 * 4896, 10, 'jrdb.Race.odds_trifecta', 4896)
    ]
