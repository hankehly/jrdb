import json
from abc import ABC
from dataclasses import dataclass
from typing import Optional, Union, Any, Callable, Tuple, Dict

import numpy as np
import pandas as pd
from django.apps import apps

MODEL_ITEM_FIELD_MAP: Dict[str, Tuple[str]] = {
    'IntegerItem': ('PositiveSmallIntegerField', 'SmallIntegerField', 'PositiveIntegerField'),
    'FloatItem': ('FloatField',),
    'StringItem': ('CharField', 'TextField', 'ForeignKey'),
    'DateItem': ('DateField',),
    'ForeignKeyItem': ('ForeignKey',),
    'DateTimeItem': ('DateTimeField',),
    'ChoiceItem': ('CharField',),
    'ArrayItem': ('ArrayField',),
    'BooleanItem': ('BooleanField', 'NullBooleanField')
}


def parse_int_or(value: str, default: Optional[Any] = None) -> Optional[int]:
    try:
        return int(value)
    except ValueError:
        return default


def parse_float_or(value: str, default: Optional[Any] = None) -> Optional[float]:
    try:
        return float(value)
    except ValueError:
        return default


def lower_first(value: str) -> str:
    assert isinstance(value, str)
    return value[:1].lower() + value[1:] if value else ''


@dataclass(eq=False, frozen=True)
class Item(ABC):
    label: str
    width: int
    start: int

    @property
    def key(self) -> str:
        return self.label

    def transform(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        raise NotImplementedError

    def _validate(self) -> None:
        assert self.width >= 0, 'width must be greater than or equal to 0'
        assert self.start >= 0, 'start must be greater than or equal to 0'


@dataclass(eq=False, frozen=True)
class ModelItem(Item, ABC):
    symbol: str

    @property
    def key(self) -> str:
        value = self.symbol.split('.', maxsplit=1).pop()
        return lower_first(value).replace('.', '__')

    def get_model(self) -> Any:
        model, _ = self.symbol.rsplit('.', maxsplit=1)
        return apps.get_model(model)

    def get_field(self) -> Any:
        _, field = self.symbol.rsplit('.', maxsplit=1)
        return self.get_model()._meta.get_field(field)

    def _validate(self) -> None:
        super()._validate()
        assert len(self.symbol.split('.')) == 3, f'invalid symbol <{self.symbol}>'
        assert self.get_field().get_internal_type() in MODEL_ITEM_FIELD_MAP.get(self.__class__.__name__), (
            f"field <name: {self.get_field().name}, type: {self.get_field().get_internal_type()}> "
            f"not found in MODEL_ITEM_FIELD_MAP['{self.__class__.__name__}']"
        )


@dataclass(eq=False, frozen=True)
class IntegerItem(ModelItem):
    default: Optional[int] = None

    def transform(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()
        return s.apply(parse_int_or, args=(self.default,)).astype('Int64')


@dataclass(eq=False, frozen=True)
class FloatItem(ModelItem):
    default: Optional[float] = np.nan
    scale: float = 1.

    def transform(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()
        return s.apply(parse_float_or, args=(self.default,)).apply(lambda n: n * self.scale).astype(float)


@dataclass(eq=False, frozen=True)
class ArrayItem(ModelItem):
    size: int
    mapper: Callable = None

    @property
    def element_width(self) -> int:
        return int(self.width / self.size)

    @property
    def base_field(self):
        return self.get_field().base_field

    def transform(self, se: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()

        base_field_type = self.base_field.get_internal_type()

        se = se.copy()
        if base_field_type in MODEL_ITEM_FIELD_MAP['IntegerItem']:
            se = se.apply(lambda a: [int(el) if el.isdigit() else None for el in map(str.strip, a)])
        elif base_field_type in MODEL_ITEM_FIELD_MAP['FloatItem']:
            se = se.apply(lambda a: [parse_float_or(item) for item in a])
        else:
            se = se.map(list).map(lambda lst: [None if x.replace(' ', '') == '' else x for x in lst])

        if self.mapper:
            se = se.apply(lambda arr: [self.mapper(item) for item in arr])

        return se.apply(json.dumps).str.replace('[', '{').str.replace(']', '}')

    def _validate(self) -> None:
        super()._validate()
        assert self.size >= 0, f'size must be greater than or equal to zero <size: {self.size}>'
        assert self.width % self.size == 0, f'width must be divisible by size <width: {self.width}, size: {self.size}>'


@dataclass(eq=False, frozen=True)
class ForeignKeyItem(ModelItem):
    related_symbol: str

    @property
    def key(self) -> str:
        key = super(ForeignKeyItem, self).key
        return '_'.join([key, self.get_remote_field().name])

    def get_remote_field(self):
        model, field = self.related_symbol.rsplit('.', maxsplit=1)
        return apps.get_model(model)._meta.get_field(field)

    def transform(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()
        remote_field = self.get_remote_field()

        remote_records = remote_field.model.objects \
            .filter(**{f'{remote_field.name}__in': s}) \
            .values(remote_field.name, 'id')

        model_name = self.get_model()._meta.model_name
        field_name = self.get_field().column
        index_name = '__'.join((model_name, field_name))

        return s.map({record[remote_field.name]: record['id'] for record in remote_records}) \
            .astype('Int64') \
            .rename(index_name)

    def _validate(self) -> None:
        super()._validate()
        assert len(self.related_symbol.split('.')) == 3, f'invalid related symbol <{self.related_symbol}>'


@dataclass(eq=False, frozen=True)
class DateItem(ModelItem):
    format: str = '%Y%m%d'

    def transform(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()
        date = pd.to_datetime(s, format=self.format, errors='coerce').dt.date.astype(str)
        return date.astype(object).where(date.notnull(), None)


@dataclass(eq=False, frozen=True)
class DateTimeItem(ModelItem):
    format: str = '%Y%m%d%H%M'
    tz: str = 'Asia/Tokyo'

    def transform(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()
        return pd.to_datetime(s, format=self.format).dt.tz_localize(self.tz).astype(str).rename(self.key)


@dataclass(eq=False, frozen=True)
class StringItem(ModelItem):

    def transform(self, se: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()
        return se.str.strip().str.replace('\u3000', ' ').mask(lambda string: string == '', None)


@dataclass(eq=False, frozen=True)
class ChoiceItem(ModelItem):
    options: dict

    def transform(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()
        return s.str.strip().map(self.options)


@dataclass(eq=False, frozen=True)
class BooleanItem(ModelItem):
    value_true: str = '1'
    value_false: str = '0'

    def transform(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()
        return s.str.strip().map({self.value_true: True, self.value_false: False})


@dataclass(eq=False, frozen=True)
class InvokeItem(Item):
    handler: Callable

    def transform(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        self._validate()
        return self.handler(s)
