import os
from os import path
import sqlite3

from .link import Link


class Links(object):
    def __init__(self):
        self._links = {}

    def add(self, link):
        self._links[link.url] = link

    def find_by_tag(self, tag):
        return [link for link in self._links.values() if tag in link.tags]

    def get_all(self):
        return self._links.values()

    def remove(self, link):
        del self._links[link.url]

    def find_by_url(self, url):
        return self._links[url]


class SqliteLinks(object):
    def __init__(self, table_gateways):
        self._links_table = table_gateways['links']
        self._tags_table = table_gateways['tags']

    def add(self, link):
        self._links_table.save(link.url, link.date)
        self._tags_table.reset_tags(link.url, link.tags)

    def find_by_tag(self, tag):
        found = []
        for url in self._tags_table.get_urls_of_links_with_tag(tag):
            date = self._links_table.get_date(url)
            tags = self._tags_table.get_tags(url)

            found.append(Link(url, tags, date))

        return found

    def get_all(self):
        all_links = []
        for url, date in self._links_table.get_all():
            tags = self._tags_table.get_tags(url)

            all_links.append(Link(url, tags, date))

        return all_links

    def remove(self, link):
        self._tags_table.remove_tags(link.url)
        self._links_table.remove_url_and_date(link.url)

    def find_by_url(self, url):
        date = self._links_table.get_date(url)
        tags = self._tags_table.get_tags(url)

        return Link(url, tags, date)



class SqliteTable(object):
    def __init__(self, sqlite_connection):
        self._connection = sqlite_connection

        self._set_up()

    def _set_up(self):
        with self._connection as connection:
            connection.execute(self.SQL_COMMAND_FOR_TABLE_CREATION)


class LinksTable(SqliteTable):
    SQL_COMMAND_FOR_TABLE_CREATION = '''
        create table if not exists links(
            url
                primary key
                not null,
            date_saved
                not null
        )
    '''

    def get_all(self):
        with self._connection as connection:
            return connection.execute('select url, date_saved from links').fetchall()

    def save(self, url, date):
        with self._connection as connection:
            connection.execute(
                'insert or ignore into links(url, date_saved) values(?, ?)',
                (url, date)
            )

    def get_date(self, url):
        with self._connection as connection:
            row = connection.execute(
                'select date_saved from links where url = ?',
                (url,)
            ).fetchone()
            date = row[0]

            return date

    def remove_url_and_date(self, url):
        with self._connection as connection:
            connection.execute('delete from links where url = ?', (url,))


class TagsTable(SqliteTable):
    SQL_COMMAND_FOR_TABLE_CREATION = '''
        create table if not exists tags(
            url
                not null,
            name
                not null,

            foreign key(url) references links(url)
                on delete restrict
                on update restrict
            )
    '''

    def get_urls_of_links_with_tag(self, tag):
        with self._connection as connection:
            list_of_rows = connection.execute(
                'select url from tags where name = ?',
                (tag,)
            ).fetchall()

            return tuple(url for (url,) in list_of_rows)

    def get_tags(self, url):
        with self._connection as connection:
            list_of_rows = connection.execute(
                'select name from tags where url = ?',
                (url,)
            ).fetchall()

            return tuple(tag for (tag,) in list_of_rows)

    def reset_tags(self, url, tags):
        self.remove_tags(url)
        self.add_tags(url, tags)

    def remove_tags(self, url):
        with self._connection as connection:
            connection.execute('delete from tags where url = ?', (url,))

    def add_tags(self, url, tags):
        with self._connection as connection:
            connection.executemany(
                'insert into tags(url, name) values(?, ?)',
                [(url, tag) for tag in tags]
            )



class SqliteConnectionFactory(object):
    @staticmethod
    def create_autoclosing_on_disk():
        return AutoclosingSqliteConnection()

    @classmethod
    def create_in_memory(cls):
        connection_to_in_memory_database = sqlite3.connect(':memory:')
        cls._enable_enforcement_of_foreign_key_constraints(connection_to_in_memory_database)

        return connection_to_in_memory_database

    @staticmethod
    def _enable_enforcement_of_foreign_key_constraints(sqlite_connection):
        sqlite_connection.execute('pragma foreign_keys = on')

    @classmethod
    def create_on_disk(cls, data_directory):
        connection_to_on_disk_database = sqlite3.connect(data_directory.path_to_database_file)
        cls._enable_enforcement_of_foreign_key_constraints(connection_to_on_disk_database)

        return connection_to_on_disk_database


class AutoclosingSqliteConnection(object):
    def __init__(self, provider_of_sqlite_connection=None):
        self._provider_of_sqlite_connection = provider_of_sqlite_connection if provider_of_sqlite_connection is not None \
            else ProviderOfConnectionToOnDiskSqliteDatabase()

    def __enter__(self):
        self._current_connection = self._provider_of_sqlite_connection.get()
        self._current_connection.__enter__()

        return self._current_connection

    def __exit__(self, type_, value, traceback):
        self._current_connection.__exit__(type_, value, traceback)
        self._current_connection.close()

        return False


class ProviderOfConnectionToOnDiskSqliteDatabase(object):
    def __init__(self):
        self._directory = ApplicationDataDirectory()

    def get(self):
        return SqliteConnectionFactory.create_on_disk(self._directory)


class ApplicationDataDirectory(object):
    @property
    def path(self):
        return path.expanduser('~/.linkstore/')

    @property
    def name_of_database_file(self):
        return 'linkstore.sqlite'

    @property
    def path_to_database_file(self):
        self._ensure_data_directory_exists()

        return path.join(self.path, self.name_of_database_file)

    def _ensure_data_directory_exists(self):
        if path.exists(self.path):
            return

        os.mkdir(self.path)
