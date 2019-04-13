import logging

from django.db import IntegrityError, transaction

from jrdb.models import Race
from jrdb.templates.item import ForeignKeyItem, IntegerItem, StringItem, ArrayItem
from jrdb.templates.parse import filter_na
from jrdb.templates.template import Template

logger = logging.getLogger(__name__)


class OZ(Template):
    """
    http://www.jrdb.com/program/Oz/Ozdata_doc.txt
    http://www.jrdb.com/program/Oz/Ozsiyo_doc.txt
    """
    name = 'JRDB基準オッズデータ（OZ）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Race.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Race.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Race.round'),
        StringItem('日', 1, 5, 'jrdb.Race.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('登録頭数', 2, 8, 'jrdb.Race.contender_count'),
        ArrayItem('単勝オッズ', 5 * 18, 10, 'jrdb.Race.odds_win', 18),
        ArrayItem('複勝オッズ', 5 * 18, 100, 'jrdb.Race.odds_show', 18),
        ArrayItem('連勝オッズ', 5 * 153, 190, 'jrdb.Race.odds_quinella', 153),
    ]

    @transaction.atomic
    def persist(self):
        df = self.clean()
        for row in df.to_dict('records'):
            race = filter_na(row)

            unique_key = {
                'racetrack_id': race.pop('racetrack_id'),
                'yr': race.pop('yr'),
                'round': race.pop('round'),
                'day': race.pop('day'),
                'num': race.pop('num')
            }

            try:
                Race.objects.update_or_create(**unique_key, defaults=race)
            except IntegrityError as e:
                logger.exception(e)
