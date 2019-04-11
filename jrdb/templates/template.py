import logging
from abc import ABC
from pprint import pprint
from typing import List, Any

import numpy as np
import pandas as pd

from jrdb.templates.item import ArrayItem

logger = logging.getLogger(__name__)


class Template(ABC):
    name = ''
    items = []

    def __init__(self, path):
        self.path = path
        self._df = None

    @property
    def df(self) -> pd.DataFrame:
        if isinstance(self._df, pd.DataFrame):
            return self._df
        raise ValueError(f'{self.__class__.__name__}.df is invalid. Please run {self.__class__.__name__}.parse.')

    @df.setter
    def df(self, value: pd.DataFrame):
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
