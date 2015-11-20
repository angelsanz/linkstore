import os
from os import path
import sqlite3


class SqliteLinkStorage(object):
    def __init__(self, in_memory=False):
        connection_to_database = SqliteConnectionFactory.create(in_memory)

        self.links_table = LinksTable(connection_to_database)

    def get_all(self):
        return self.links_table.get_all()

    def save(self, an_url, a_tag):
        self.links_table.save(an_url, a_tag)

    def find_by_tag(self, a_tag):
        return self.links_table.find_by_tag(a_tag)


class SqliteConnectionFactory(object):
    @staticmethod
    def create(in_memory):
        if in_memory:
            return sqlite3.connect(':memory:')

        return AutoclosingSqliteConnection()


class LinksTable(object):
    def __init__(self, connection_to_database):
        self._connection = connection_to_database

        self._set_up_table()

    def _set_up_table(self):
        with self._connection as connection:
            connection.execute('create table if not exists links(link_id integer primary key, url, tag)')

    def get_all(self):
        with self._connection as connection:
            return connection.execute('select url, tag from links') \
                .fetchall()

    def save(self, an_url, a_tag):
        with self._connection as connection:
            connection.execute('insert into links(url, tag) values(?, ?)', (an_url, a_tag))

    def find_by_tag(self, a_tag):
        with self._connection as connection:
            return connection.execute('select url, tag from links where tag = ?', (a_tag,)) \
                .fetchall()


class AutoclosingSqliteConnection(object):
    def __init__(self, provider_of_sqlite_connection=None):
        self._provider_of_sqlite_connection = provider_of_sqlite_connection if provider_of_sqlite_connection is not None  \
            else ProviderOfConnectionToOnDiskSqliteDatabase()

    def __enter__(self):
        self._current_connection = self._provider_of_sqlite_connection.get()
        self._current_connection.__enter__()

        return self._current_connection

    def __exit__(self, type, value, traceback):
        self._current_connection.__exit__(type, value, traceback)
        self._current_connection.close()

        return False


class ProviderOfConnectionToOnDiskSqliteDatabase(object):
    def __init__(self):
        self._directory = ApplicationDataDirectory()

    def get(self):
        return sqlite3.connect(self._directory.path_to_database_file)


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
