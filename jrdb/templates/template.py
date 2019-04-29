import logging
from abc import ABC
from typing import List, Any, Union, Iterable

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


# WIP
# class ModelPersistMixin:
#     SEP = ','
#
#     def get_model(self, symbol: str):
#         model, _ = symbol.rsplit('.', maxsplit=1)
#         return apps.get_model(model)
#
#     def unique_together(self, symbol):
#         # Assumes only 1 combination
#         model = self.get_model(symbol)
#         return [
#             model._meta.get_field(field).attname
#             for field in model._meta.unique_together[0]
#         ]
#
#     def persist_model(self, symbol):
#         prefix = f'{self.get_model(symbol).model_name}__'
#         df = self.clean.pipe(startswith, prefix, rename=True)
#
#         cols = self.SEP.join('"{}"'.format(key) for key in df.columns)
#         vals = self.SEP.join(map(str, map(tuple, df.values))).replace('nan', 'NULL')
#
#         uniq = self.unique_together(symbol)
#         uniq_str = self.SEP.join('"{}"'.format(key) for key in uniq)
#         updates = self.SEP.join((f'{key}=excluded.{key}' for key in df.columns if key not in uniq))
#
#         sql = (
#             f'INSERT INTO programs ({cols}) '
#             f'VALUES {vals} '
#         )
#
#         if updates:
#             sql += f'ON CONFLICT ({uniq_str}) DO UPDATE SET {updates}'
#         else:
#             sql += f'ON CONFLICT DO NOTHING'
#
#         with connection.cursor() as c:
#             c.execute(sql)


class PersistHelper:
    SEP = ','

    def fmt_cols(self, symbol: str):
        prefix = apps.get_model(symbol)._meta.model_name
        df = self.clean.pipe(startswith, prefix, rename=True)
        return '(' + self.SEP.join('"{}"'.format(key) for key in df.columns) + ')'

    def fmt_vals(self, symbol: str):
        prefix = apps.get_model(symbol)._meta.model_name
        df = self.clean.pipe(startswith, prefix, rename=True)
        return self.SEP.join(map(str, map(tuple, df.values))).replace('nan', 'NULL')


class ProgramRacePersistMixin(PersistHelper):
    SEP = ','

    def as_comma_sep_str(self, a: Iterable) -> str:
        return ','.join('"{}"'.format(key) for key in a)

    def as_comma_sep_tuples_str(self, a: Iterable) -> str:
        return ','.join(map(str, map(tuple, a)))

    def persist(self):
        pdf = self.clean.pipe(startswith, 'program__', rename=True)

        pcol = self.as_comma_sep_str(pdf.columns)
        pval = self.as_comma_sep_tuples_str(pdf.drop_duplicates().values)

        with connection.cursor() as c:
            c.execute(f'INSERT INTO programs ({pcol}) VALUES {pval} ON CONFLICT DO NOTHING')

        programs = pd.DataFrame(
            Program.objects
                   .filter(racetrack_id__in=pdf.racetrack_id, yr__in=pdf.yr, round__in=pdf['round'], day__in=pdf.day)
                   .values('id', 'racetrack_id', 'yr', 'round', 'day')
        )

        rdf = self.clean.pipe(startswith, 'race__', rename=True)
        rdf['program_id'] = pdf.merge(programs).id

        rcol = self.as_comma_sep_str(rdf.columns)
        rval = self.as_comma_sep_tuples_str(rdf.values)

        rupd = self.SEP.join((f'{key}=excluded.{key}' for key in rdf.columns if key not in ['program_id', 'num']))

        sql = (
            f'INSERT INTO races ({rcol}) VALUES {rval} ON CONFLICT (program_id, num) DO UPDATE SET {rupd}'
            .replace('nan', 'NULL')
        )

        with connection.cursor() as c:
            c.execute(sql)

    # def persist(self):
    #     pdf = self.clean.pipe(startswith, 'program__', rename=True)
    #
    #     pcol = self.as_comma_sep_str(pdf.columns)
    #     pval = self.as_comma_sep_tuples_str(pdf.drop_duplicates().values)
    #
    #     rdf = self.clean.pipe(startswith, 'race__', rename=True)
    #     rcol = self.as_comma_sep_str(['program_id'] + rdf.columns.tolist())
    #
    #     program_idx = [
    #         f"(SELECT id FROM programs WHERE racetrack_id = {row.racetrack_id} AND yr = {row.yr} AND round = {row.round} AND day = '{row.day}')"
    #         for row in pdf.itertuples()
    #     ]
    #
    #     rval = self.as_comma_sep_tuples_str(np.c_[program_idx, rdf.values]).replace('"(', '(').replace(')"', ')')
    #     rupd = self.SEP.join((f'{key}=excluded.{key}' for key in rdf.columns if key not in ['program_id', 'num']))
    #
    #     sql = (
    #         f'WITH '
    #         f'  cte AS ( '
    #         f'      INSERT INTO programs ({pcol}) VALUES {pval} '
    #         f'      ON CONFLICT DO NOTHING '
    #         f'  ) '
    #         f'INSERT INTO races ({rcol}) VALUES {rval} '
    #         f'ON CONFLICT (program_id, num) DO UPDATE SET {rupd}'
    #     ).replace('nan', 'NULL').replace('NaN', 'NULL')
    #     # import ipdb; ipdb.set_trace()
    #     with connection.cursor() as c:
    #         c.execute(sql)
    #
    # def persist_(self):
    #     """
    #     Django implementation (for speed comparison)
    #     """
    #     from ..models import Program, Race
    #     for _, row in self.clean.iterrows():
    #         program_dct = row.pipe(startswith, 'program__', rename=True).dropna().to_dict()
    #         program_unique_keys = ['racetrack_id', 'yr', 'round', 'day']
    #         program_lookup = {key: value for key, value in program_dct.items() if key in program_unique_keys}
    #         program, _ = Program.objects.get_or_create(**program_lookup)
    #
    #         race_dct = row.pipe(startswith, 'race__', rename=True).dropna().to_dict()
    #         race_lookup = {'program_id': program.id, 'num': race_dct.get('num')}
    #         race_defaults = {key: value for key, value in race_dct.items() if key != 'num'}
    #         race, _ = Race.objects.update_or_create(**race_lookup, defaults=race_defaults)


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
