import logging
from abc import ABC
from typing import List, Any, Union

import numpy as np
import pandas as pd
from django.db import transaction, IntegrityError, connection

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

    # def persist(self):
    #     df = self.clean().pipe(startswith, 'program__', rename=True)
    #
    #     columns = ','.join('"{}"'.format(key) for key in df.columns)
    #     values = ','.join(map(str, map(tuple, df.values))).replace('nan', 'NULL')
    #
    #     unique_together = ['racetrack_id', 'yr', 'round', 'day']
    #     conflict = ','.join('"{}"'.format(key) for key in unique_together)
    #     updates = ', '.join((f'{key}=excluded.{key}' for key in df.columns if key not in unique_together))
    #
    #     sql = (
    #         f'INSERT INTO programs ({columns}) '
    #         f'VALUES {values} '
    #         f'ON CONFLICT ({conflict}) '
    #         f'DO UPDATE SET {updates}'
    #     )
    #
    #     with connection.cursor() as c:
    #         c.execute(sql)

    @transaction.atomic
    def persist(self):
        from ..models import Program
        for _, row in self.clean().iterrows():
            program_dct = row.pipe(startswith, 'program__', rename=True).dropna().to_dict()
            program_unique_keys = ['racetrack_id', 'yr', 'round', 'day']
            program_lookup = {key: value for key, value in program_dct.items() if key in program_unique_keys}
            program, _ = Program.objects.get_or_create(**program_lookup)

            race_dct = row.pipe(startswith, 'race__', rename=True).dropna().to_dict()
            race_lookup = {'program_id': program.id, 'num': race_dct.get('num')}
            race_defaults = {key: value for key, value in race_dct.items() if key != 'num'}
            race, _ = Race.objects.update_or_create(**race_lookup, defaults=race_defaults)


def startswith(
        f: Union[pd.Series, pd.DataFrame],
        prefix: str,
        rename: bool = False
) -> Union[pd.Series, pd.DataFrame]:
    f = f.copy()
    axis = 'columns' if isinstance(f, pd.DataFrame) else 'index'
    names = [name for name in getattr(f, axis) if name.startswith(prefix)]
    f = f[names]
    if rename:
        f = f.rename(**{axis: lambda name: name[len(prefix):] if name.startswith(prefix) else name})
    f.prefix = prefix
    return f
