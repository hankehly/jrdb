import logging
from abc import ABC
from pprint import pprint
from typing import List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class Template(ABC):
    name = ''
    items = []

    def __init__(self, filepath):
        self.filepath = filepath
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
    def spec(self) -> pd.DataFrame:
        df = pd.DataFrame(self.items, columns=['key', 'label', 'OCC', 'width', 'type', 'startpos', 'notes'])
        df.OCC = df.OCC.fillna(1).astype(int)
        df.width = df.width.astype(int)
        df.startpos = df.startpos.astype(int) - 1
        df.notes = df.notes.fillna('')
        df.name = self.name
        return df

    @property
    def colnames(self) -> List[str]:
        """
        Provide a list of str column names that match self.df column count.
        By default, OCC > 1 items have an index appended to the key name (ie. key_0, key_1, etc..)
        """
        cols = []
        for row in self.spec.itertuples():
            if row.OCC > 1:
                for i in range(1, row.OCC + 1):
                    cols.append(f'{row.key}_{i}')
            else:
                cols.append(row.key)
        return cols

    def parse(self) -> pd.DataFrame:
        """
        Parse contents of self.filepath into DataFrame

        Using the slightly slower np.char.decode(byterows, encoding='cp932') rather than decoding
        each cell individually to make parsing less of a hassle for subclasses
        """
        self._validate()
        with open(self.filepath, 'rb') as f:
            byterows = []
            lines = filter(None, f.read().splitlines())
            for line in lines:
                byterow = []
                for spec in self.spec.itertuples():
                    byterow.extend(self.parse_item(line, spec))
                byterows.append(byterow)
        encoded_rows = np.char.decode(byterows, encoding='cp932')
        self.df = pd.DataFrame(encoded_rows, columns=self.colnames)
        return self.df

    def parse_item(self, line, spec) -> List:
        """
        Given a byte string (line) and a spec item (spec)
        return an array of on or more byte strings where each item matches a specific column

        Unless the item OCC is greater than 1, the return value will be a single-item list
        """
        row = []
        if spec.OCC > 1:
            for j in range(spec.OCC):
                start = spec.startpos + (spec.width * j)
                stop = start + spec.width
                cell = line[start:stop]
                row.append(cell)
        else:
            start = spec.startpos
            stop = spec.startpos + spec.width
            cell = line[start:stop]
            row.append(cell)
        return row

    def persist(self) -> None:
        raise NotImplementedError

    @classmethod
    def _validate(cls, raise_on_invalid=True) -> bool:
        invalid_idx = [str(i) for i, item in enumerate(cls.items) if len(item) != 7]
        if invalid_idx:
            idx_list = ', '.join(invalid_idx)
            if raise_on_invalid:
                raise ValueError(f'Check following indices: {idx_list}')
            return False
        return True


def parse_template(path):
    """
    Helper function for developer to extract template rows from data doc files
    and print them as lists

    Exported rows may contain missing information (OCC field, notes)
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

        startpos = None
        for i, line in enumerate(nonnull_fields):
            if line[0] == '項目名':
                startpos = i + 1
                break

        endpos = None
        for i, line in enumerate(nonnull_fields[startpos:], startpos):
            if '**' in line[0]:
                endpos = i
                break

        template_fields = [field for field in nonnull_fields[startpos:endpos] if len(field) > 3]
        pprint(template_fields)
