import re
from typing import List, Any

import pandas as pd
from django.apps import apps
from django.db import connection
from django.db.models import Q
from django.utils.functional import cached_property

from .template import startswith


class Loader:
    def load(self):
        raise NotImplementedError


class DjangoPostgresUpsertLoader(Loader):

    def __init__(self, df: pd.DataFrame, app_label: str, model_name: str = None, index_predicate: str = None) -> None:
        self.df = df
        self.app_label = app_label
        self.model_name = model_name
        self.index_predicate = index_predicate

    @cached_property
    def model(self) -> Any:
        return apps.get_model(self.app_label, self.model_name)

    @cached_property
    def unique_columns(self) -> List[str]:
        """
        Assumes:
            - unique keys are listed in unique_together
            - only 1 unique index
        """
        cols = []
        if self.model._meta.unique_together:
            cols = [self.model._meta.get_field(name).attname for name in self.model._meta.unique_together[0]]
        return cols

    def _build_insert(self) -> str:
        columns = ','.join('"{}"'.format(key) for key in self.df.columns)

        values_dirty = ','.join(map(str, map(tuple, self.df.values)))
        values = re.sub(r'(None|nan|NaN|\'NaT\')', 'NULL', values_dirty).replace(',)', ')')

        return ' '.join([
            f'INSERT INTO {self.model._meta.db_table} ({columns})',
            f'VALUES {values}'
        ])

    def _build_conflict(self) -> str:
        update_cols = ','.join([f'{key}=EXCLUDED.{key}' for key in self.df.columns if key not in self.unique_columns])
        conflict_target = ','.join('"{}"'.format(key) for key in self.unique_columns)

        sql = 'ON CONFLICT'
        if conflict_target and update_cols:
            sql = ' '.join([sql, f'({conflict_target}) DO UPDATE SET {update_cols}'])
        else:
            sql = ' '.join([sql, 'DO NOTHING'])

        if self.index_predicate:
            sql = ' '.join([sql, 'WHERE', self.index_predicate])

        return sql

    def _build_sql(self):
        return ' '.join([
            self._build_insert(),
            self._build_conflict()
        ])

    def _result_queryset(self):
        lookup = None
        for kwargs in self.df[self.unique_columns].to_dict('records'):
            if lookup is None:
                lookup = Q(**kwargs)
            else:
                lookup = lookup | Q(**kwargs)
        return self.model.objects.filter(lookup).values('id', *self.unique_columns)

    def load(self):
        sql = self._build_sql()
        with connection.cursor() as c:
            c.execute(sql)
        return self._result_queryset()


class ProgramRaceLoadMixin:

    def load(self):
        pdf = self.transform.pipe(startswith, 'program__', rename=True)
        programs = self.loader_cls(pdf, 'jrdb.Program').load().to_dataframe()
        rdf = self.transform.pipe(startswith, 'race__', rename=True)
        rdf['program_id'] = pdf.merge(programs, how='left').id
        self.loader_cls(rdf, 'jrdb.Race').load()
