from .item import ForeignKeyItem, IntegerItem, StringItem, ArrayItem
from .template import ProgramRacePersistMixin, Template


class OW(Template, ProgramRacePersistMixin):
    """
    http://www.jrdb.com/program/Oz/Owdata_doc.txt
    """
    name = 'ワイド基準オッズデータ（OW）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('登録頭数', 2, 8, 'jrdb.Race.contender_count'),
        ArrayItem('ワイドオッズ', 5 * 153, 10, 'jrdb.Race.odds_duet', 153),
    ]
