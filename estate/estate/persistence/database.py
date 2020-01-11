from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from ..settings import ESTATE_DB_CONNECTION_CONFIG


class MySqlEngine(object):
    def __init__(self):
        self.__db_engine = create_engine(
            ESTATE_DB_CONNECTION_CONFIG,
            max_overflow=0,     # maximum number of connections to allow in connection_pool `overflow`
            pool_size=5,        # connection pool size
            pool_timeout=30,    # time to wait before getting a connection
            pool_recycle=-1,    # recycle connection after `x` seconds, (-1, means never)
        )

        __session_factory = sessionmaker(
            bind=self.__db_engine
        )
        self.__Session = scoped_session(
            __session_factory
        )
        self.Model = declarative_base()

    @property
    def session(self):
        """support multi-threads safety
        """
        return self.__Session

    def create_all_tables(self):
        last_pos = ESTATE_DB_CONNECTION_CONFIG.rfind('/')

        with create_engine(
                ESTATE_DB_CONNECTION_CONFIG[:last_pos]
        ).connect() as connection:
            connection.execute(
                'CREATE DATABASE IF NOT EXISTS `wonder` DEFAULT CHARACTER SET utf8mb4'
            )

        self.Model.metadata.create_all(
            self.__db_engine, checkfirst=True
        )

    def drop_all_tables(self):
        self.Model.metadata.drop_all(
            self.__db_engine
        )


db = MySqlEngine()
