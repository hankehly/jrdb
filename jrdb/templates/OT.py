import logging

from django.db import transaction, IntegrityError

from jrdb.templates.item import ForeignKeyItem, IntegerItem, StringItem, ArrayItem
from jrdb.templates.parse import filter_na
from jrdb.templates.template import Template
from jrdb.models import Race

logger = logging.getLogger(__name__)


class OT(Template):
    """
    http://www.jrdb.com/program/Ot/Otdata_doc.txt
    """
    name = '３連複基準オッズデータ（OT）'
    items = [
        ForeignKeyItem('場コード', 2, 0, 'jrdb.Race.racetrack', 'jrdb.Racetrack.code'),
        IntegerItem('年', 2, 2, 'jrdb.Race.yr'),
        IntegerItem('回', 1, 4, 'jrdb.Race.round'),
        StringItem('日', 1, 5, 'jrdb.Race.day'),
        IntegerItem('Ｒ', 2, 6, 'jrdb.Race.num'),
        IntegerItem('登録頭数', 2, 8, 'jrdb.Race.contender_count'),
        ArrayItem('３連複オッズ', 6 * 816, 10, 'jrdb.Race.odds_trio', 816),
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
