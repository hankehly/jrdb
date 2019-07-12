from .item import ForeignKeyItem, IntegerItem, StringItem, ArrayItem
from ..loaders import ProgramRaceLoadMixin
from .template import Template


class OT(Template, ProgramRaceLoadMixin):
    """
    http://www.jrdb.com/program/Ot/Otdata_doc.txt
    """
    description = '３連複基準オッズデータ（OT）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('登録頭数', 2, 8, 'jrdb.Race.contender_count'),
        ArrayItem('３連複オッズ', 6 * 816, 10, 'jrdb.Race.odds_trio', 816),
    ]
