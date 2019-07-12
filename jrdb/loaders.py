from typing import List, Any, Callable, Optional

import pandas as pd
from django.apps import apps
from django.utils.functional import cached_property
from sqlalchemy import select, or_, and_
from sqlalchemy.dialects.postgresql import insert

from .store import store
from .templates.template import startswith


class DjangoPostgresUpsertLoader:
    def __init__(
        self, df: pd.DataFrame, app_label: str, model_name: str = None
    ) -> None:
        self.df = df
        self.app_label = app_label
        self.model_name = model_name

    @cached_property
    def model(self) -> Any:
        return apps.get_model(self.app_label, self.model_name)

    @cached_property
    def table(self):
        return store[self.model._meta.db_table]

    @cached_property
    def unique_columns(self) -> List[str]:
        """
        Assumes
         - unique keys are listed in unique_together
         - only 1 unique index exists
        """
        cols = []
        if self.model._meta.unique_together:
            cols = [
                self.model._meta.get_field(name).attname
                for name in self.model._meta.unique_together[0]
            ]
        return cols

    @cached_property
    def _data(self) -> pd.DataFrame:
        indices = self.df[self.unique_columns].drop_duplicates().index
        df = self.df.loc[indices]

        # Forcibly upcast values to prevent type errors
        values = df.to_numpy()

        # Convert all nan values to None. This is work for the transform layer;
        # but that change requires returning multidimensional arrays of scalar values
        # as opposed to pandas objects.
        isna = df.isna().to_numpy()
        values[isna] = None

        return pd.DataFrame(values, columns=df.columns)

    def _build_upsert(self, where: Optional[Callable] = None):
        """
        To print a representation of this SQL in the console
        specify the postgresql dialect during compilation

        >>> from sqlalchemy.dialects import postgresql
        >>> print(insert_stmt.compile(dialect=postgresql.dialect()))
        """
        values = self._data.to_dict("records")
        insert_stmt = insert(self.table).values(values)

        set_ = {
            col: getattr(insert_stmt.excluded, col)
            for col in self._data.columns
            if col not in self.unique_columns
        }

        where_stmt = where(insert_stmt) if where else None

        if set_:
            return insert_stmt.on_conflict_do_update(
                index_elements=self.unique_columns, set_=set_, where=where_stmt
            )

        return insert_stmt.on_conflict_do_nothing(index_elements=self.unique_columns)

    def _build_select(self):
        groups = []
        for row in self._data.itertuples():
            conditions = and_(
                *[
                    getattr(self.table.c, col) == getattr(row, col)
                    for col in self.unique_columns
                ]
            )
            groups.append(conditions)

        columns = [
            getattr(self.table.c, column) for column in ["id"] + self.unique_columns
        ]
        whereclause = or_(*groups)

        return select(columns).where(whereclause)

    def load(self, where: Optional[Callable] = None) -> pd.DataFrame:
        upsert_stmt = self._build_upsert(where)
        select_stmt = self._build_select()

        with store.engine.connect() as conn:
            conn.execute(upsert_stmt)
            rows = conn.execute(select_stmt)

        columns = ["id"] + self.unique_columns
        return pd.DataFrame(rows, columns=columns)


class ProgramRaceLoadMixin:
    def load_programs_races(self):
        pdf = self.transform.pipe(startswith, "program__", rename=True)
        programs = self.loader_cls(pdf, "jrdb.Program").load()
        rdf = self.transform.pipe(startswith, "race__", rename=True)
        rdf["program_id"] = pdf.merge(programs, how="left").id
        self.loader_cls(rdf, "jrdb.Race").load()
