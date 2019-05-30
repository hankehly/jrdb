from django.db import connection
from django.utils.functional import cached_property
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine.url import URL


class SQLAlchemyModelStore:

    def __init__(self):
        self._tables = {}

    @cached_property
    def engine(self):
        cnf = connection.settings_dict
        url = URL(connection.vendor, cnf['USER'], cnf['PASSWORD'], cnf['HOST'], cnf['PORT'], cnf['NAME'])
        return create_engine(url)

    @cached_property
    def meta(self):
        return MetaData(bind=self.engine)

    def __getitem__(self, item):
        if item in self._tables:
            return self._tables[item]
        return Table(item, self.meta, autoload=True)


store = SQLAlchemyModelStore()
