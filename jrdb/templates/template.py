import logging
from abc import ABC
from typing import List, Any

import numpy as np
import pandas as pd
from django.db import transaction, IntegrityError

from ..models import Race
from .item import ArrayItem

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
                    bytes_lst = self.parse_item(line, item)
                    str_lst = np.char.decode(bytes_lst, encoding='cp932')
                    if len(str_lst) == 1:
                        row.append(str_lst[0])
                    else:
                        row.append(str_lst)
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
        objs = []
        for col in self.df:
            item = next(item for item in self.items if item.key == col)
            objs.append(item.clean(self.df[col]))
        return pd.concat(objs, axis='columns')


# TODO: Use model._meta to automate lookup and persistence
class RacePersistMixin:

    @transaction.atomic
    def persist(self):
        df = self.clean().pipe(select_columns_startwith, 'race__', rename=True)

        for _, row in df.iterrows():
            race = row.dropna().to_dict()
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


def select_columns_startwith(df: pd.DataFrame, prefix: str, rename: bool = False) -> pd.DataFrame:
    df = df.copy()
    cols = [col for col in df.columns if col.startswith(prefix)]
    df = df[cols]
    if rename:
        df = df.rename(columns=lambda col: col[len(prefix):] if col.startswith(prefix) else col)
    df.prefix = prefix
    return df


def select_index_startwith(se: pd.Series, prefix: str, rename: bool = False) -> pd.Series:
    se = se.copy()
    names = [name for name in se.index if name.startswith(prefix)]
    se = se[names]
    if rename:
        se = se.rename(index=lambda name: name[len(prefix):] if name.startswith(prefix) else name)
    se.prefix = prefix
    return se
