from abc import ABC
from typing import List, Any

import numpy as np
import pandas as pd
from django.utils.functional import cached_property

from .item import ArrayItem


class Template(ABC):
    name = ''
    items = []

    def __init__(self, path):
        self.path = path
        self.df = None

    @cached_property
    def loader_cls(self):
        # TODO: Lazy load to prevent import errors
        from ..loaders import DjangoPostgresUpsertLoader
        return DjangoPostgresUpsertLoader

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
                    lst_bytes = self.extract_item(line, item)
                    lst_str = np.char.decode(lst_bytes, encoding='cp932')
                    if len(lst_str) == 1:
                        row.append(lst_str[0])
                    else:
                        row.append(lst_str)
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
