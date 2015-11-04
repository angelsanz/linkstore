import os
from os import path
import sqlite3


class SqliteLinkStorage(object):
    def __init__(self, in_memory=False):
        self._connection = SqliteConnectionFactory.create(in_memory)
        self._set_up_database()

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


class SqliteConnectionFactory(object):
    @staticmethod
    def create(in_memory):
        if in_memory:
            return sqlite3.connect(':memory:')

        return AutoclosingSqliteConnection()


class AutoclosingSqliteConnection(object):
    def __init__(self):
        self._application_data_directory = ApplicationDataDirectory()

    def __enter__(self):
        self._current_connection = self._create_new_connection()
        self._current_connection.__enter__()

        return self._current_connection

    def _create_new_connection(self):
        return sqlite3.connect(self._application_data_directory.path_to_database_file)

    def __exit__(self, type, value, traceback):
        self._current_connection.__exit__(type, value, traceback)
        self._current_connection.close()

        return False


class ApplicationDataDirectory(object):
    def __init__(self):
        self.path_to_data_directory = path.expanduser('~/.linkstore/')
        name_of_database_file = 'linkstore.sqlite'
        self._path_to_database_file = path.join(self.path_to_data_directory, name_of_database_file)

    @property
    def path_to_database_file(self):
        self._ensure_data_directory_exists()

        return self._path_to_database_file

    def _ensure_data_directory_exists(self):
        if path.exists(self.path_to_data_directory):
            return

        os.mkdir(self.path_to_data_directory)


class InMemoryLinkStorage(object):
    def __init__(self):
        self._links = []

    def get_all(self):
        return self._links

    def save(self, an_url, a_tag):
        self._links.append((an_url, a_tag))

    def find_by_tag(self, a_tag):
        return [ link for link in self.get_all() if link[1] == a_tag ]
