from typing import List, Any

import pandas as pd
from django.apps import apps
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
        return create_engine(url)

    @cached_property
    def table(self):
        return Table(self.model._meta.db_table, self.meta, autoload=True, autoload_with=self.engine)

    @cached_property
    def unique_columns(self) -> List[str]:
        """
        Makes the following assumptions
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
        To print a representation of this SQL in the console, specify the correct dialect
        >>> from sqlalchemy.dialects import postgresql
        >>> print(sql.compile(dialect=postgresql.dialect()))
        """
        indices = self.df[self.unique_columns].drop_duplicates().index
        df = self.df.iloc[indices]

        # upcast values to prevent psycopg2 type errors due to numpy dtype values
        records = df.to_numpy()

        # Convert all nan values to None. This is work for the transform layer.
        # Making that change will require returning multidimensional arrays of generic data,
        # rather than pandas objects
        isnull = df.isna().to_numpy()
        records[isnull] = None

        values = pd.DataFrame(records, columns=df.columns).to_dict('records')

        ins = insert(self.table).values(values)
        ins_cols = {col: getattr(ins.excluded, col) for col in df.columns if col not in self.unique_columns}

        if ins_cols:
            return ins.on_conflict_do_update(index_elements=self.unique_columns, set_=ins_cols)

        return ins.on_conflict_do_nothing(index_elements=self.unique_columns)

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
        # sqlalchemy
        upsert = self._build_sql_sa()
        select = self._build_select()
        with self.engine.connect() as conn:
            conn.execute(upsert)
            rows = conn.execute(select)
            columns = ['id'] + self.unique_columns
            data = pd.DataFrame(rows, columns=columns)
        self.engine.dispose()
        return data


class ProgramRaceLoadMixin:

    def load(self):
        pdf = self.transform.pipe(startswith, 'program__', rename=True)
        programs = self.loader_cls(pdf, 'jrdb.Program').load()
        rdf = self.transform.pipe(startswith, 'race__', rename=True)
        rdf['program_id'] = pdf.merge(programs, how='left').id
        self.loader_cls(rdf, 'jrdb.Race').load()
