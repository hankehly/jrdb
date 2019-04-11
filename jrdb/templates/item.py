import re
from abc import ABC
from dataclasses import dataclass
from typing import Optional, Union, Any, Callable, Tuple, Dict, List

import numpy as np
import pandas as pd
from django.apps import apps

MODEL_ITEM_FIELD_MAP: Dict[str, Tuple[str]] = {
    'IntegerItem': ('PositiveSmallIntegerField', 'SmallIntegerField', 'PositiveIntegerField'),
    'StringItem': ('CharField', 'TextField'),
    'DateItem': ('DateField',),
    'ForeignKeyItem': ('ForeignKey',),
    'DateTimeItem': ('DateTimeField',),
    'ChoiceItem': ('CharField',),
    'ArrayItem': ('ArrayField',)
}


@dataclass(eq=False, frozen=True)
class Item(ABC):
    label: str
    width: int
    start: int

    def __post_init__(self):
        self._validate()

    @property
    def key(self) -> str:
        return self.label

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        raise NotImplementedError

    def _validate(self) -> None:
        assert self.width >= 0, 'width must be greater than or equal to 0'
        assert self.start >= 0, 'start must be greater than or equal to 0'


@dataclass(eq=False, frozen=True)
class ModelItem(Item, ABC):
    symbol: str

    @property
    def key(self) -> str:
        return self.symbol.split('.').pop()

    def get_model(self) -> Any:
        model, _ = self.symbol.rsplit('.', maxsplit=1)
        return apps.get_model(model)

    def get_field(self) -> Any:
        _, field = self.symbol.rsplit('.', maxsplit=1)
        return self.get_model()._meta.get_field(field)

    def _validate(self) -> None:
        super()._validate()
        assert len(self.symbol.split('.')) == 3
        assert self.get_field().get_internal_type() in MODEL_ITEM_FIELD_MAP.get(self.__class__.__name__)


@dataclass(eq=False, frozen=True)
class IntegerItem(ModelItem):

    @classmethod
    def _parse_int_or(cls, value: str, default=None) -> Optional[int]:
        try:
            return int(value)
        except ValueError:
            return default

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        return s.apply(self._parse_int_or, args=(np.nan,)).astype('Int64')


@dataclass(eq=False, frozen=True)
class ArrayItem(ModelItem):
    """
    It would be nicer to figure this out dynamically by the width

    TODO: Handle non-integer types
    """
    # base_type: int
    size: int

    @property
    def element_width(self) -> int:
        return int(self.width / self.size)

    def _parse_integer_list(self, value) -> List[int]:
        regexp = r'.{' + str(self.size) + r'}'
        matches = map(str.strip, re.findall(regexp, value))
        return [int(match) if match.isdigit() else 0 for match in matches]

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        return s.apply(self._parse_integer_list)

    def _validate(self) -> None:
        super()._validate()
        assert self.size >= 0, f'size must be greater than or equal to zero <size: {self.size}>'
        assert self.width % self.size == 0, f'width must be divisible by size <width: {self.width}, size: {self.size}>'


@dataclass(eq=False, frozen=True)
class ForeignKeyItem(ModelItem):
    related_symbol: str

    def get_remote_field(self):
        model, field = self.related_symbol.rsplit('.', maxsplit=1)
        return apps.get_model(model)._meta.get_field(field)

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        field = self.get_field()

        if hasattr(field.remote_field.model, 'key2id'):
            return field.remote_field.model.key2id(s).rename(field.column)

        remote_field_name = self.get_remote_field().name

        remote_records = field.remote_field.model.objects \
            .filter(**{f'{remote_field_name}__in': s}) \
            .values(remote_field_name, 'id')

        return s.map({record[remote_field_name]: record['id'] for record in remote_records}) \
            .rename(field.column)

    def _validate(self) -> None:
        super()._validate()
        assert len(self.related_symbol.split('.')) == 3


@dataclass(eq=False, frozen=True)
class DateItem(ModelItem):
    format: str = '%Y%m%d'

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        return pd.to_datetime(s, format=self.format).dt.date


@dataclass(eq=False, frozen=True)
class DateTimeItem(ModelItem):
    format: str = '%Y%m%d%H%M'
    tz: str = 'Asia/Tokyo'

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        return pd.to_datetime(s, format=self.format).dt.tz_localize(self.tz).rename(self.key)


@dataclass(eq=False, frozen=True)
class StringItem(ModelItem):

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        return s.str.strip()


@dataclass(eq=False, frozen=True)
class ChoiceItem(ModelItem):
    options: dict

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        return s.str.strip().map(self.options)


@dataclass(eq=False, frozen=True)
class InvokeItem(Item):
    handler: Callable

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        return self.handler(s)
