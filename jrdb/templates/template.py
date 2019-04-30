import logging
from abc import ABC
from typing import List, Any, Union

import numpy as np
import pandas as pd
from django.apps import apps
from django.db import connection
from django.utils.functional import cached_property

from ..models import Program
from .item import ArrayItem

logger = logging.getLogger(__name__)


class Template(ABC):
    name = ''
    items = []

    def __init__(self, path):
        self.path = path
        self._df = None
        self._clean_df = None

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

    @cached_property
    def clean(self) -> pd.DataFrame:
        objs = []
        for col in self.df:
            item = next(item for item in self.items if item.key == col)
            objs.append(item.clean(self.df[col]))
        return pd.concat(objs, axis='columns')


class PostgresUpsertMixin:

    def get_foreign_key_fields(self, symbol: str):
        meta = apps.get_model(symbol)._meta
        unique_together = meta.unique_together[0] if meta.unique_together else []

        return [
            meta.get_field(field) for field in unique_together if
            meta.get_field(field).is_relation and hasattr(meta.get_field(field).remote_field, 'model')
        ]

    def upsert(self, app_label_model_name: str, **kwargs):
        meta = apps.get_model(app_label_model_name)._meta

        prefix = meta.model_name + '__'
        df = self.clean.pipe(startswith, prefix, rename=True)

        for field in self.get_foreign_key_fields(app_label_model_name):
            if field.attname in kwargs:
                df[field.attname] = kwargs[field.attname]

        df.drop_duplicates(inplace=True)

        columns = ','.join('"{}"'.format(key) for key in df.columns)

        values = (
            ','.join(map(str, map(tuple, df.values)))
                .replace('nan', 'NULL')
                .replace('NaN', 'NULL')
                .replace('\'NaT\'', 'NULL')
                .replace(',)', ')')
        )

        sql = f'INSERT INTO {meta.db_table} ({columns}) VALUES {values}'

        unique_fields = meta.unique_together[0] if meta.unique_together else []
        conflict_fields = [meta.get_field(field).attname for field in unique_fields]
        conflict_target = ','.join('"{}"'.format(key) for key in conflict_fields)
        update_columns = ','.join((f'{key}=EXCLUDED.{key}' for key in df.columns if key not in conflict_fields))

        if conflict_target and update_columns:
            sql += f'ON CONFLICT ({conflict_target}) DO UPDATE SET {update_columns} '
        else:
            sql += 'ON CONFLICT DO NOTHING '

        if 'index_predicate' in kwargs:
            sql += ' '.join(('WHERE', kwargs['index_predicate']))

        with connection.cursor() as c:
            c.execute(sql)


class ProgramRacePersistMixin(PostgresUpsertMixin):

    def persist(self):
        self.upsert('jrdb.Program')

        pdf = self.clean.pipe(startswith, 'program__', rename=True)

        programs = pd.DataFrame(
            Program.objects
                .filter(racetrack_id__in=pdf.racetrack_id, yr__in=pdf.yr, round__in=pdf['round'], day__in=pdf.day)
                .values('id', 'racetrack_id', 'yr', 'round', 'day')
        )

        self.upsert('jrdb.Race', program_id=pdf.merge(programs).id)


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
