import logging
import re
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
        self._transform_df = None

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            raise ValueError(f'{self.__class__.__name__}.df is invalid. Please run {self.__class__.__name__}.extract.')
        return self._df

    @df.setter
    def df(self, value):
        if not isinstance(value, pd.DataFrame):
            raise ValueError(f'df must be type DataFrame, got {type(value)}')
        self._df = value

    def extract(self) -> 'Template':
        """
        Extract contents of self.path into DataFrame

        Using the slightly slower np.char.decode(byterows, encoding='cp932') rather than decoding
        each cell individually to make parsing less of a hassle for subclasses
        """
        with open(self.path, 'rb') as f:
            rows = []
            lines = filter(None, f.read().splitlines())
            for line in lines:
                row = []
                for item in self.items:
                    bytes_lst = self.extract_item(line, item)
                    str_lst = np.char.decode(bytes_lst, encoding='cp932')
                    if len(str_lst) == 1:
                        row.append(str_lst[0])
                    else:
                        row.append(str_lst)
                rows.append(row)
        self.df = pd.DataFrame(rows, columns=[item.key for item in self.items])
        return self

    def extract_item(self, line: bytes, item: Any) -> List[bytes]:
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
    def transform(self) -> pd.DataFrame:
        objs = []
        for col in self.df:
            item = next(item for item in self.items if item.key == col)
            objs.append(item.transform(self.df[col]))
        return pd.concat(objs, axis='columns')


class DjangoUpsertMixin:
    """
    A class to handle SQL upsert queries.
    """

    def _get_unique_together(self, symbol: str):
        meta = apps.get_model(symbol)._meta
        return meta.unique_together[0] if meta.unique_together else []

    def _get_foreign_key_fields(self, symbol: str):
        meta = apps.get_model(symbol)._meta
        unique_together = self._get_unique_together(symbol)

        return [
            meta.get_field(field) for field in unique_together if
            meta.get_field(field).is_relation and hasattr(meta.get_field(field).remote_field, 'model')
        ]

    def _build_insert_df(self, symbol: str, **kwargs):
        prefix = apps.get_model(symbol)._meta.model_name + '__'
        df = self.transform.pipe(startswith, prefix, rename=True)

        for field in self._get_foreign_key_fields(symbol):
            if field.attname in kwargs:
                df[field.attname] = kwargs[field.attname]

        return df.drop_duplicates()

    def _format_values_string(self, string: str) -> str:
        return re.sub(r'(None|nan|NaN)', 'NULL', string).replace('\'NaT\'', 'NULL').replace(',)', ')')

    def upsert(self, symbol: str, **kwargs):
        """
        Perform postgres INSERT ... ON CONFLICT upsert

        :param symbol: app_label "." model_name
        :param kwargs:
            foreign key series (ex. {'program_id': pd.Series([1, 1, 1, 2, 2, 2, ...])})
            conflict action predicate (the WHERE clause)
        :return: A values QuerySet<Model> containing only unique identifier keys
        """
        df = self._build_insert_df(symbol, **kwargs)

        # gather query data
        model = apps.get_model(symbol)
        columns = ','.join('"{}"'.format(key) for key in df.columns)

        values_dirty = ','.join(map(str, map(tuple, df.values)))
        values = self._format_values_string(values_dirty)

        unique_columns = [model._meta.get_field(field).attname for field in self._get_unique_together(symbol)]
        conflict_target = ','.join('"{}"'.format(key) for key in unique_columns)
        update_columns = ','.join((f'{key}=excluded.{key}' for key in df.columns if key not in unique_columns))

        # build SQL query
        sql = f'INSERT INTO {model._meta.db_table} ({columns}) VALUES {values}'
        if conflict_target and update_columns:
            sql += f'ON CONFLICT ({conflict_target}) DO UPDATE SET {update_columns} '
        else:
            sql += 'ON CONFLICT DO NOTHING '
        if 'index_predicate' in kwargs:
            sql += ' '.join(('WHERE', kwargs['index_predicate']))

        with connection.cursor() as c:
            c.execute(sql)

        # TODO: Fetch only records with matching attribute combinations
        lookup = {f'{name}__in': df[name].tolist() for name in unique_columns}
        return model.objects.filter(**lookup).values('id', *unique_columns)


class ProgramRaceLoadMixin(DjangoUpsertMixin):

    def load(self):
        pdf = self.transform.pipe(startswith, 'program__', rename=True)
        programs = self.upsert('jrdb.Program').to_dataframe()
        program_id = pdf.merge(programs, how='left').id
        self.upsert('jrdb.Race', program_id=program_id)


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
