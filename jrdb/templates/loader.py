import re
from typing import List, Any

import pandas as pd
from django.apps import apps
from django.conf import settings
from django.db import connection
from django.utils.functional import cached_property
from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.postgresql import insert

from .template import startswith


class DjangoPostgresUpsertLoader:

    def __init__(self, df: pd.DataFrame, app_label: str, model_name: str = None, index_predicate: str = None) -> None:
        self.df = df
        self.app_label = app_label
        self.model_name = model_name
        self.index_predicate = index_predicate
        self.meta = MetaData()

    @cached_property
    def model(self) -> Any:
        return apps.get_model(self.app_label, self.model_name)

    @cached_property
    def engine(self):
        db = connection.settings_dict
        url = URL(connection.vendor, db['USER'], db['PASSWORD'], db['HOST'], db['PORT'], db['NAME'])
        return create_engine(url, echo=settings.DEBUG)

    @cached_property
    def table(self):
        return Table(self.model._meta.db_table, self.meta, autoload=True, autoload_with=self.engine)

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

    def _build_sql_sa(self):
        """
        Build UPSERT SQL string with SQLAlchemy Core

        To print a representation of this SQL in the console, do the following
        >>> from sqlalchemy.dialects import postgresql
        >>> print(sql.compile(dialect=postgresql.dialect()))

        This should print somthing similar to the following
        INSERT INTO programs (yr, round, day, racetrack_id)
        VALUES (%(yr_m0)s, %(round_m0)s, %(day_m0)s, %(racetrack_id_m0)s),
               (%(yr_m1)s, %(round_m1)s, %(day_m1)s, %(racetrack_id_m1)s)
        ON CONFLICT (racetrack_id, yr, round, day)
        DO NOTHING

        More information at
        https://docs.sqlalchemy.org/en/13/faq/sqlexpressions.html#stringifying-for-specific-databases
        """
        df = self.df.drop_duplicates()

        # forcibly upcast values to prevent psycopg2 type errors
        # due to numpy dtype values
        records = df.to_numpy()
        values = pd.DataFrame(records, columns=df.columns).to_dict('records')

        ins = insert(self.table).values(values)
        ins_cols = {col: getattr(ins.excluded, col) for col in df.columns if col not in self.unique_columns}

        if ins_cols:
            return ins.on_conflict_do_update(index_elements=self.unique_columns, set_=ins_cols)

        return ins.on_conflict_do_nothing(index_elements=self.unique_columns)

    def _build_insert(self) -> str:
        columns = ','.join('"{}"'.format(key) for key in self.df.columns)

        values_dirty = ','.join(map(str, map(tuple, self.df.drop_duplicates().values)))
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

    def _build_upsert(self) -> str:
        return ' '.join([
            self._build_insert(),
            self._build_conflict()
        ])

    def _build_select(self) -> str:
        def escape(val):
            return f"'{val}'" if isinstance(val, str) else val

        where = []
        df = self.df[self.unique_columns].drop_duplicates()
        for row in df.itertuples():
            sub_condition = [f'{col}={escape(getattr(row, col))}' for col in df.columns]
            condition = ' AND '.join(sub_condition)
            where.append(f'({condition})')
        where = ' OR '.join(where)

        columns = ['id'] + self.unique_columns
        columns = ','.join(columns)

        return (
            f'SELECT {columns} '
            f'FROM {self.model._meta.db_table} '
            f'WHERE {where}'
        )

    def load(self) -> pd.DataFrame:
        # with self.engine.connect() as conn:
        #     upsert = self._build_sql_sa()
        #     conn.execute(upsert)
        upsert = self._build_upsert()
        select = self._build_select()
        with connection.cursor() as c:
            c.execute(upsert)
            c.execute(select)
            rows = c.fetchall()
            columns = [col[0] for col in c.description]
            return pd.DataFrame(rows, columns=columns)


class ProgramRaceLoadMixin:

    def load(self):
        pdf = self.transform.pipe(startswith, 'program__', rename=True)
        programs = self.loader_cls(pdf, 'jrdb.Program').load()
        rdf = self.transform.pipe(startswith, 'race__', rename=True)
        rdf['program_id'] = pdf.merge(programs, how='left').id
        self.loader_cls(rdf, 'jrdb.Race').load()
