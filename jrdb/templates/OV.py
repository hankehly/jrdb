from .item import ArrayItem, IntegerItem, StringItem, ForeignKeyItem
from ..loaders import ProgramRaceLoadMixin
from .template import Template


class OV(Template, ProgramRaceLoadMixin):
    """
    http://www.jrdb.com/program/Ov/ovdata_doc.txt
    """

    description = "３連単基準オッズデータ（OV）"
    items = [
        ForeignKeyItem("場コード", 2, 0, "jrdb.Program.racetrack", "jrdb.Racetrack.code"),
        IntegerItem("年", 2, 2, "jrdb.Program.yr"),
        IntegerItem("回", 1, 4, "jrdb.Program.round"),
        StringItem("日", 1, 5, "jrdb.Program.day"),
        IntegerItem("Ｒ", 2, 6, "jrdb.Race.num"),
        IntegerItem("登録頭数", 2, 8, "jrdb.Race.contender_count"),
        ArrayItem(
            "３連単オッズ",
            7 * 4896,
            10,
            "jrdb.Race.odds_trifecta",
            4896,
            lambda n: None if n is None else round(n * 0.1, 1),
        ),
    ]

    def load(self) -> None:
        return self.load_programs_races()
