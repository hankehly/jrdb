import logging
from abc import ABC
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)

COLS = ['key', 'label', 'OCC', 'width', 'type', 'startpos', 'comment']


class DocType(ABC):
    name = ''
    items = []

    def __init__(self, filepath):
        self.filepath = filepath
        self._df = None

    @property
    def df(self):
        if isinstance(self._df, pd.DataFrame):
            return self._df.copy()
        logger.warning(f'{self.__class__.__name__}.df is not set. Please run {self.__class__.__name__}.parse first.')
        return None

    @df.setter
    def df(self, value):
        self._df = value

    @property
    def spec(self) -> pd.DataFrame:
        df = pd.DataFrame(self.items, columns=COLS)
        df.OCC = df.OCC.fillna(1).astype(int)
        df.width = df.width.astype(int)
        df.startpos = df.startpos.astype(int) - 1
        df.comment = df.comment.fillna('')
        df.name = self.name
        return df

    @property
    def colnames(self) -> List[str]:
        cols = []
        offset = 1
        for row in self.spec.itertuples():
            if row.OCC > 1:
                for i in range(offset, row.OCC + offset):
                    cols.append(f'{row.key}_{i}')
            else:
                cols.append(row.key)
        return cols

    def parse(self) -> pd.DataFrame:
        """
        Parse contents of self.filepath into DataFrame

        It is slightly faster to decode each cell individually than use
        np.char.decode(byterows, encoding='cp932')
        """
        self._validate()
        with open(self.filepath, 'rb') as f:
            rows = []
            for line in filter(None, f.read().splitlines()):
                row = []
                for item in self.spec.itertuples():
                    if item.OCC > 1:
                        for j in range(item.OCC):
                            start = item.startpos + (item.width * j)
                            stop = start + item.width
                            cell = line[start:stop].decode('cp932')
                            row.append(cell)
                    else:
                        start = item.startpos
                        stop = item.startpos + item.width
                        cell = line[start:stop].decode('cp932')
                        row.append(cell)
                rows.append(row)
        df = pd.DataFrame(rows, columns=self.colnames)
        self.df = df
        return df

    def _validate(self, raise_on_invalid=True) -> bool:
        invalid_idx = [str(i) for i, item in enumerate(self.items) if len(item) != 7]
        if invalid_idx:
            idx_list = ', '.join(invalid_idx)
            if raise_on_invalid:
                raise ValueError(f'invalid item indices: {idx_list}')
            return False
        return True


def parse_template(path):
    """
    Helper function for developer to extract template rows from data doc files
    and print them as lists

    Exported rows may contain missing information (OCC field, comments)
    and incorrectly parsed comment strings
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
        for field in template_fields:
            print(field)
