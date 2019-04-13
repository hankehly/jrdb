from abc import ABC
from dataclasses import dataclass
from typing import Optional, Union, Any, Callable, Tuple, Dict

import pandas as pd
from django.apps import apps

MODEL_ITEM_FIELD_MAP: Dict[str, Tuple[str]] = {
    'IntegerItem': ('PositiveSmallIntegerField', 'SmallIntegerField', 'PositiveIntegerField'),
    'FloatItem': ('FloatField',),
    'StringItem': ('CharField', 'TextField'),
    'DateItem': ('DateField',),
    'ForeignKeyItem': ('ForeignKey',),
    'DateTimeItem': ('DateTimeField',),
    'ChoiceItem': ('CharField',),
    'ArrayItem': ('ArrayField',)
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
        assert len(self.symbol.split('.')) == 3, f'invalid symbol <{self.symbol}>'
        assert self.get_field().get_internal_type() in MODEL_ITEM_FIELD_MAP.get(self.__class__.__name__), \
            f"field <name: {self.get_field().name}, type: {self.get_field().get_internal_type()}> " + \
            f"not found in MODEL_ITEM_FIELD_MAP['{self.__class__.__name__}']"


@dataclass(eq=False, frozen=True)
class IntegerItem(ModelItem):
    default: Optional[int] = None

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        if self.get_field().null:
            return s.apply(parse_int_or, args=(self.default,)).astype('Int64')

        return s.astype(int)


@dataclass(eq=False, frozen=True)
class FloatItem(ModelItem):
    default: Optional[float] = None

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        if self.get_field().null:
            return s.apply(parse_float_or, args=(self.default,)).astype(float)

        return s.astype(float)


@dataclass(eq=False, frozen=True)
class ArrayItem(ModelItem):
    size: int

    @property
    def element_width(self) -> int:
        return int(self.width / self.size)

    @property
    def base_field(self):
        return self.get_field().base_field

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        # TODO: Make clean logic from other items reusable in ArrayItem.clean
        base_field_type = self.base_field.get_internal_type()

        if base_field_type in MODEL_ITEM_FIELD_MAP['IntegerItem']:
            return s.apply(lambda a: [int(el) if el.isdigit() else 0 for el in map(str.strip, a)])
        elif base_field_type in MODEL_ITEM_FIELD_MAP['FloatItem']:
            return s.apply(lambda a: pd.Series(a).apply(parse_float_or).tolist())

        return s

    def _validate(self) -> None:
        super()._validate()
        assert self.size >= 0, f'size must be greater than or equal to zero <size: {self.size}>'
        assert self.width % self.size == 0, f'width must be divisible by size <width: {self.width}, size: {self.size}>'


@dataclass(eq=False, frozen=True)
class ForeignKeyItem(ModelItem):
    related_symbol: str

    @property
    def key(self) -> str:
        return self.get_field().name + '_' + self.get_remote_field().name

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
        assert len(self.related_symbol.split('.')) == 3, f'invalid related symbol <{self.related_symbol}>'


@dataclass(eq=False, frozen=True)
class DateItem(ModelItem):
    format: str = '%Y%m%d'

    def clean(self, s: pd.Series) -> Union[pd.Series, pd.DataFrame]:
        return pd.to_datetime(s, format=self.format, errors='coerce').dt.date


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