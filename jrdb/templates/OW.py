from .item import ForeignKeyItem, IntegerItem, StringItem, ArrayItem
from .OZ import OZ


class OW(OZ):
    """
    http://www.jrdb.com/program/Oz/Owdata_doc.txt
    """
    name = 'ワイド基準オッズデータ（OW）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Race.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Race.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Race.round'),
        StringItem('日', 1, 5, 'jrdb.Race.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('登録頭数', 2, 8, 'jrdb.Race.contender_count'),
        ArrayItem('ワイドオッズ', 5 * 153, 10, 'jrdb.Race.odds_duet', 153),
    ]
