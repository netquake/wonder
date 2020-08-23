from os import path as file_path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from ...spider import SingaporeAgents
from .contacts import Contacts


class MySqlEngine(object):
    def __init__(self):
        self.__db_engine = create_engine(
            SingaporeAgents.SQLITE3_CONNECTION,
            echo=True
        )

        __session_factory = sessionmaker(
            bind=self.__db_engine
        )
        self.__session = scoped_session(
            __session_factory
        )
        self.Model = declarative_base()

    @property
    def session(self):
        """support multi-threads safety
        """
        return self.__session

    def create_all_tables(self):
        db_file_path = SingaporeAgents.SQLITE3_CONNECTION.replace(
            'sqlite:///', ''
        )

        if not file_path.exists(db_file_path):

            self.Model.metadata.create_all(
                self.__db_engine, checkfirst=True
            )

    def drop_all_tables(self):
        self.Model.metadata.drop_all(
            self.__db_engine
        )


db = MySqlEngine()
