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
