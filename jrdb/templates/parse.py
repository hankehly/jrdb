import datetime
import re
from typing import Optional, List

import numpy as np
import pandas as pd


def parse_date(value, format) -> Optional[datetime.date]:
    try:
        return datetime.datetime.strptime(value, format).date()
    except ValueError:
        return None


def parse_comma_separated_integer_list(value, n) -> List[int]:
    regexp = r'.{' + str(n) + r'}'
    matches = map(str.strip, re.findall(regexp, value))
    return [int(m) if m.isdigit() else 0 for m in matches]


def parse_int_or(value: str, default=None) -> Optional[int]:
    try:
        return int(value)
    except ValueError:
        return default


def parse_float_or(value: str, default=None) -> Optional[float]:
    try:
        return float(value)
    except ValueError:
        return default


def filter_na(obj: dict) -> dict:
    return {k: v for k, v in obj.items() if v not in [None, np.nan, pd.NaT]}


def lower_first(value: str) -> str:
    assert isinstance(value, str)
    return value[:1].lower() + value[1:] if value else ''


def select_columns_startwith(df: pd.DataFrame, prefix: str, rename: bool = False) -> pd.DataFrame:
    df = df.copy()

    cols = [col for col in df.columns if col.startswith(prefix)]
    df = df[cols]

    if rename:
        df = df.rename(columns=lambda col: col[len(prefix):] if col.startswith(prefix) else col)

    df.prefix = prefix
    return df


def select_index_startwith(se: pd.Series, prefix: str, rename: bool = False) -> pd.Series:
    se = se.copy()
    names = [name for name in se.index if name.startswith(prefix)]
    se = se[names]
    if rename:
        se = se.rename(index=lambda name: name[len(prefix):] if name.startswith(prefix) else name)
    se.prefix = prefix
    return se


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
