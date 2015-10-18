import os
from os import path
import sqlite3


class SqliteLinkStorage(object):
    DATABASE_FILE_NAME = 'linkstore.sqlite'
    PATH_TO_DATA_DIRECTORY = path.expanduser('~/.linkstore')
    PATH_TO_DATABASE = path.join(PATH_TO_DATA_DIRECTORY, DATABASE_FILE_NAME)

    def __init__(self, in_memory=False):
        if in_memory:
            self._connection = sqlite3.connect(':memory:')
        else:
            self._ensure_data_directory_exists()
            self._connection = sqlite3.connect(SqliteLinkStorage.PATH_TO_DATABASE)

        self._set_up_database()

    def _ensure_data_directory_exists(self):
        if path.exists(SqliteLinkStorage.PATH_TO_DATA_DIRECTORY):
            return

        os.mkdir(SqliteLinkStorage.PATH_TO_DATA_DIRECTORY)

    def _set_up_database(self):
        with self._connection as connection:
            connection.execute('create table if not exists links(url, tag)')

    def get_all(self):
        with self._connection as connection:
            return connection.execute('select * from links') \
                .fetchall()

    def save(self, an_url, a_tag):
        with self._connection as connection:
            connection.execute('insert into links values(?, ?)', (an_url, a_tag))

    def find_by_tag(self, a_tag):
        with self._connection as connection:
            return connection.execute('select * from links where tag = ?', (a_tag,)) \
                .fetchall()


class InMemoryLinkStorage(object):
    def __init__(self):
        self._links = []

    def get_all(self):
        return self._links

    def save(self, an_url, a_tag):
        self._links.append((an_url, a_tag))

    def find_by_tag(self, a_tag):
        return [ link for link in self.get_all() if link[1] == a_tag ]
