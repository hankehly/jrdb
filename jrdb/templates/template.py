import logging
from abc import ABC
from typing import List, Any

import numpy as np
import pandas as pd
from django.db import transaction, IntegrityError

from ..models import Race
from .item import ArrayItem
from .parse import filter_na

logger = logging.getLogger(__name__)


class Template(ABC):
    name = ''
    items = []

    def __init__(self, path):
        self.path = path
        self._df = None

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            raise ValueError(f'{self.__class__.__name__}.df is invalid. Please run {self.__class__.__name__}.parse.')
        return self._df

    @df.setter
    def df(self, value):
        if not isinstance(value, pd.DataFrame):
            raise ValueError(f'df must be type DataFrame, got {type(value)}')
        self._df = value

    def parse(self) -> 'Template':
        """
        Parse contents of self.path into DataFrame

        Using the slightly slower np.char.decode(byterows, encoding='cp932') rather than decoding
        each cell individually to make parsing less of a hassle for subclasses
        """
        with open(self.path, 'rb') as f:
            rows = []
            lines = filter(None, f.read().splitlines())
            for line in lines:
                row = []
                for item in self.items:
                    parsed = self.parse_item(line, item)
                    encoded = np.char.decode(parsed, encoding='cp932')
                    if len(encoded) == 1:
                        row.append(encoded[0])
                    else:
                        row.append(encoded)
                rows.append(row)
        self.df = pd.DataFrame(rows, columns=[item.key for item in self.items])
        return self

    def parse_item(self, line: bytes, item: Any) -> List[bytes]:
        row = []
        if isinstance(item, ArrayItem):
            for i in range(item.size):
                start = item.start + (item.element_width * i)
                stop = start + item.element_width
                cell = line[start:stop]
                row.append(cell)
        else:
            stop = item.start + item.width
            cell = line[item.start:stop]
            row.append(cell)
        return row

    def clean(self) -> pd.DataFrame:
        arr = []
        for name in self.df:
            item = next(item for item in self.items if item.key == name)
            arr.append(item.clean(self.df[name]))
        return pd.concat(arr, axis='columns')

    def persist(self) -> None:
        raise NotImplementedError


class RacePersistMixin:

    @transaction.atomic
    def persist(self):
        for row in self.clean().to_dict('records'):
            race = filter_na(row)
            lookup = {
                'racetrack_id': race.pop('racetrack_id'),
                'yr':           race.pop('yr'),
                'round':        race.pop('round'),
                'day':          race.pop('day'),
                'num':          race.pop('num')
            }
            try:
                Race.objects.update_or_create(**lookup, defaults=race)
            except IntegrityError as e:
                logger.exception(e)
