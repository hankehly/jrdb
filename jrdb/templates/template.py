import dataclasses
import logging
from abc import ABC
from pprint import pprint
from typing import List

import numpy as np
import pandas as pd
from django.apps import apps

from jrdb.templates.parse import parse_int_or, parse_date

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Item:
    symbol: str
    label: str
    width: int
    start: int

    repeat: int = 0
    notes: str = ''
    use: bool = True
    options: dict = None
    date_fmt: str = ''

    @property
    def key(self):
        return self.symbol.split('.').pop()

    def get_model(self):
        model = '.'.join(self.symbol.split('.')[:2])
        return apps.get_model(model)

    def get_field(self):
        comps = self.symbol.split('.')[2:]
        return self.get_model()._meta.get_field(comps[0])

    def get_foreign_column_name(self):
        if self.get_field().get_internal_type() == 'ForeignKey':
            comps = self.symbol.split('.')
            if len(comps) == 4:
                return comps[3]
        return None


# class DateItem(Item):
#     format: str


class Template(ABC):
    name = ''
    items = []

    def __init__(self, path):
        self.path = path
        self._df = None

    @property
    def df(self) -> pd.DataFrame:
        if isinstance(self._df, pd.DataFrame):
            return self._df.copy()
        raise ValueError(f'{self.__class__.__name__}.df is invalid. Please run {self.__class__.__name__}.parse.')

    @df.setter
    def df(self, value):
        self._df = value

    @property
    def colnames(self) -> List[str]:
        """
        Provide a list of str column names that match self.df column count.
        """
        cols = []
        for item in self.items:
            cols.append(item.key)
        return cols

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
        self.df = pd.DataFrame(rows, columns=self.colnames)
        return self

    def parse_item(self, line: bytes, item: Item) -> List[bytes]:
        row = []
        if item.repeat > 0:
            for i in range(item.repeat):
                start = item.start + (item.width * i)
                stop = start + item.width
                cell = line[start:stop]
                row.append(cell)
        else:
            stop = item.start + item.width
            cell = line[item.start:stop]
            row.append(cell)
        return row

    def clean(self) -> pd.DataFrame:
        df = pd.DataFrame(index=self.df.index)

        for name in self.df:
            item = [i for i in self.items if i.key == name][0]
            if not item.use:
                continue

            handler = 'clean_' + name
            if hasattr(self, handler):
                df = df.join(getattr(self, handler)())
            else:
                field = item.get_field()
                internal_type = field.get_internal_type()
                sr = self.df[name]

                if internal_type == 'ForeignKey':
                    if hasattr(field.remote_field.model, 'key2id'):
                        df[field.column] = field.remote_field.model.key2id(sr)
                    else:
                        column = item.get_foreign_column_name()
                        remote_records = field.remote_field.model.objects \
                            .filter(**{f'{column}__in': sr}) \
                            .values(column, 'id')
                        df[field.column] = sr.map({o[column]: o['id'] for o in remote_records})
                    df[field.column].name = field.column
                elif internal_type == 'PositiveSmallIntegerField':
                    if field.null:
                        df[name] = sr.apply(parse_int_or, args=(np.nan,)).astype('Int64')
                    else:
                        df[name] = sr.astype(int)
                elif internal_type in ['CharField', 'TextField']:
                    strip = sr.str.strip()
                    if field.choices:
                        df[name] = strip.map(item.options)
                    else:
                        df[name] = strip
                elif internal_type == 'DateField':
                    df[name] = sr.apply(parse_date, args=(item.date_fmt,))

        return df

    def persist(self) -> None:
        raise NotImplementedError


def parse_template(path):
    """
    Helper function for developer to extract template rows from data doc files
    and print them as lists

    Exported rows may contain missing information (repeat field, notes)
    and incorrectly parsed notes strings

    Usage:
        $ wget http://www.jrdb.com/program/Kab/kab_doc.txt
        $ python
        >> from jrdb.templates.template import parse_template
        >> parse_template('kab_doc.txt')
    """
    with open(path, 'rb') as f:
        nonnull_fields = []
        for line in f:
            fields = line.decode('cp932').strip().split()
            if fields and len(fields) > 1:
                nonnull_fields.append(fields)

        start = None
        for i, line in enumerate(nonnull_fields):
            if line[0] == '項目名':
                start = i + 1
                break

        endpos = None
        for i, line in enumerate(nonnull_fields[start:], start):
            if '**' in line[0]:
                endpos = i
                break

        template_fields = [field for field in nonnull_fields[start:endpos] if len(field) > 3]
        pprint(template_fields)
