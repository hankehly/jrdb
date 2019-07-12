from .item import ForeignKeyItem, IntegerItem, StringItem, ArrayItem
from ..loaders import ProgramRaceLoadMixin
from .template import Template


class OZ(Template, ProgramRaceLoadMixin):
    """
    http://www.jrdb.com/program/Oz/Ozdata_doc.txt
    http://www.jrdb.com/program/Oz/Ozsiyo_doc.txt
    """
    description = 'JRDB基準オッズデータ（OZ）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Program.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Program.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Program.round'),
        StringItem('日', 1, 5, 'jrdb.Program.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('登録頭数', 2, 8, 'jrdb.Race.contender_count'),
        ArrayItem('単勝オッズ', 5 * 18, 10, 'jrdb.Race.odds_win', 18),
        ArrayItem('複勝オッズ', 5 * 18, 100, 'jrdb.Race.odds_show', 18),
        ArrayItem('連勝オッズ', 5 * 153, 190, 'jrdb.Race.odds_quinella', 153),
    ]

    def load(self) -> None:
        return self.load_programs_races()
