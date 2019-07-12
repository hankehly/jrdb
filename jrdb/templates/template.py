import os
import re
from abc import ABC
from typing import List, Any, Union

import numpy as np
import pandas as pd
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

from .item import ArrayItem


class Template(ABC):
    description = ""
    items = []

    def __init__(self, path):
        self.path = path
        self.df = None

    @cached_property
    def loader_cls(self):
        # TODO: Lazy load to prevent import errors
        from ..loaders import DjangoPostgresUpsertLoader

        return DjangoPostgresUpsertLoader

    def extract(self) -> "Template":
        """
        Extract contents of self.path into DataFrame

        Using the slightly slower np.char.decode(byterows, encoding='cp932') rather than decoding
        each cell individually to make parsing less of a hassle for subclasses
        """
        with open(self.path, "rb") as f:
            rows = []
            lines = filter(None, f.read().splitlines())
            for line in lines:
                row = []
                for item in self.items:
                    lst_bytes = self._extract_item(line, item)
                    lst_str = np.char.decode(lst_bytes, encoding="cp932")
                    if len(lst_str) == 1:
                        row.append(lst_str[0])
                    else:
                        row.append(lst_str)
                rows.append(row)
        self.df = pd.DataFrame(rows, columns=[item.key for item in self.items])
        return self

    def _extract_item(self, line: bytes, item: Any) -> List[bytes]:
        row = []
        if isinstance(item, ArrayItem):
            for i in range(item.size):
                start = item.start + (item.element_width * i)
                stop = start + item.element_width
                cell = line[start:stop]
                row.append(cell)
        else:
            stop = item.start + item.width
            cell = line[item.start : stop]
            row.append(cell)
        return row

    @cached_property
    def transform(self) -> pd.DataFrame:
        objs = []
        for col in self.df:
            item = next(item for item in self.items if item.key == col)
            objs.append(item.transform(self.df[col]))
        return pd.concat(objs, axis="columns")

    def load(self) -> None:
        pass


def startswith(
    f: Union[pd.Series, pd.DataFrame], prefix: str, rename: bool = False
) -> Union[pd.Series, pd.DataFrame]:
    f = f.copy()
    axis = "columns" if isinstance(f, pd.DataFrame) else "index"
    names = [name for name in getattr(f, axis) if name.startswith(prefix)]
    f = f[names]
    if rename:
        f = f.rename(
            **{
                axis: lambda name: name[len(prefix) :]
                if name.startswith(prefix)
                else name
            }
        )
    f.prefix = prefix
    return f


def template_factory(path: str) -> Template:
    name = extract_template_name(path)
    module_path = ".".join(["jrdb", "templates", name])
    return import_string(module_path)(path)


def extract_template_name(path):
    basename = os.path.basename(path)
    filename, _ = os.path.splitext(basename)
    name = re.search("[A-Z]+", filename).group()
    return name
