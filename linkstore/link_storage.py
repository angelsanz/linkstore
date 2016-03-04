import os
from os import path
import sqlite3

from .link import LinkRecord


class SqliteLinkStorage(object):
    def __init__(self, table_gateways):
        self._links_table = table_gateways['links']
        self._tags_table = table_gateways['tags']

    def get_all(self):
        return [
            LinkRecord(
                link_id,
                url,
                self._tags_table.get_tags_by_id(link_id),
                date_saved
            )
            for link_id, url, date_saved in self._links_table.get_all()
        ]

    def save(self, link):
        self._links_table.save(link.url, link.date)

        id_of_newly_created_link = self._links_table.get_id_by_url(link.url)
        self._tags_table.save_tags_for_link_with_id(id_of_newly_created_link, link.tags)

    def find_by_tag(self, tag):
        records_of_matching_links = []
        for link_id in self._tags_table.get_ids_of_links_with_tag(tag):
            url, date = self._links_table.get_url_and_date_by_id(link_id)

            records_of_matching_links.append(LinkRecord(link_id, url, self._tags_table.get_tags_by_id(link_id), date))

        return records_of_matching_links

    def replace_tag_in_link_with_url(self, url, tag_modification):
        id_of_relevant_link = self._links_table.get_id_by_url(url)
        self.replace_tag_in_link_with_id(id_of_relevant_link, tag_modification)

    def replace_tag_in_link_with_id(self, link_id, tag_modification):
        self._tags_table.replace_tag_in_link_with_id(link_id, tag_modification)

    def add_tags_to_link_with_url(self, url, tags):
        id_of_relevant_link = self._links_table.get_id_by_url(url)
        self.add_tags_to_link_with_id(id_of_relevant_link, tags)

    def add_tags_to_link_with_id(self, link_id, tags):
        self._tags_table.save_tags_for_link_with_id(link_id, tags)


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


class SqliteTable(object):
    def __init__(self, connection_to_database):
        self._connection = connection_to_database

        self._set_up()

    def _set_up(self):
        with self._connection as connection:
            connection.execute(self.SQL_COMMAND_FOR_TABLE_CREATION)


class LinksTable(SqliteTable):
    SQL_COMMAND_FOR_TABLE_CREATION = '''
        create table if not exists links(
            link_id integer primary key
                not null,
            url
                unique
                not null,
            date_saved
                not null
        )
    '''

    def get_all(self):
        with self._connection as connection:
            return connection.execute('select link_id, url, date_saved from links').fetchall()

    def get_id_by_url(self, url):
        with self._connection as connection:
            row_of_link_with_given_url = connection.execute(
                'select link_id from links where url = ?',
                (url,)
            ).fetchone()
            desired_id = row_of_link_with_given_url[0]

            return desired_id

    def save(self, url, date):
        with self._connection as connection:
            connection.execute(
                'insert into links(url, date_saved) values(?, ?)',
                (url, date)
            )

    def get_url_and_date_by_id(self, link_id):
        with self._connection as connection:
            return connection.execute(
                'select url, date_saved from links where link_id = ?',
                (link_id,)
            ).fetchone()


class TagsTable(SqliteTable):
    SQL_COMMAND_FOR_TABLE_CREATION = '''
        create table if not exists tags(
            link_id
                not null,
            name
                not null,

            foreign key(link_id) references links(link_id)
                on delete restrict
                on update restrict
            )
    '''

    def save_tags_for_link_with_id(self, link_id, tags):
        with self._connection as connection:
            connection.executemany(
                'insert into tags(link_id, name) values(?, ?)',
                [(link_id, tag) for tag in tags]
            )

    def get_ids_of_links_with_tag(self, tag):
        with self._connection as connection:
            list_of_rows = connection.execute(
                'select link_id from tags where name = ?',
                (tag,)
            ).fetchall()

            return (link_id for (link_id,) in list_of_rows)

    def get_tags_by_id(self, link_id):
        with self._connection as connection:
            list_of_rows = connection.execute(
                'select name from tags where link_id = ?',
                (link_id,)
            ).fetchall()

            return tuple(tag for (tag,) in list_of_rows)

    def replace_tag_in_link_with_id(self, link_id, tag_modification):
        current_tag = tag_modification.keys()[0]
        new_tag = tag_modification.values()[0]

        with self._connection as connection:
            connection.execute(
                'update tags set name = ? where link_id = ? and name = ?',
                (new_tag, link_id, current_tag)
            )


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
