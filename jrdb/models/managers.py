import pandas as pd
from django.db import models
from django.db.models.query import ModelIterable


class DataFrameQuerySet(models.QuerySet):
    def to_dataframe(self):
        records = self.values() if issubclass(self._iterable_class, ModelIterable) else self
        return pd.DataFrame.from_records(records)
