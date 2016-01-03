import os
from os import path
import sqlite3


class SqliteLinkStorage(object):
    def __init__(self, connection_to_database, clock):
        self._clock = clock

        self._links_table = LinksTable(connection_to_database)
        self._tags_table = TagsTable(connection_to_database)

    def get_all(self):
        all_links = []
        for link_id, url, date_saved in self._links_table.get_all():
            all_links.append((
                url,
                date_saved,
                self._tags_table.get_tags_of_link_with_id(link_id)
            ))

        return all_links

    def save(self, an_url, tag_or_tags):
        self._links_table.save(an_url, self._clock.date_of_today())

        id_of_newly_created_link = self._links_table.get_id_of_link_with_url(an_url)
        tags_to_save = self._pack_given_tag_or_tags(tag_or_tags)
        self._tags_table.save_tags_for_link_with_id(id_of_newly_created_link, tags_to_save)

    def _pack_given_tag_or_tags(self, tag_or_tags):
        if isinstance(tag_or_tags, basestring):
            return (tag_or_tags,)

        return tag_or_tags

    def find_by_tag(self, a_tag):
        matching_links = []
        for link_id in self._tags_table.get_ids_of_links_with_tag(a_tag):
            matching_links.append(
                self._links_table.get_url_and_date_of_link_with_id(link_id) +
                (self._tags_table.get_tags_of_link_with_id(link_id),)
            )

        return matching_links


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
    def _enable_enforcement_of_foreign_key_constraints(an_sqlite_connection):
        an_sqlite_connection.execute('pragma foreign_keys = on')

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

    def get_id_of_link_with_url(self, an_url):
        with self._connection as connection:
            row_of_link_with_given_url = connection.execute(
                'select link_id from links where url = ?',
                (an_url,)
            ).fetchone()
            desired_id = row_of_link_with_given_url[0]

            return desired_id

    def save(self, an_url, a_date):
        with self._connection as connection:
            connection.execute(
                'insert into links(url, date_saved) values(?, ?)',
                (an_url, a_date)
            )

    def get_url_and_date_of_link_with_id(self, a_link_id):
        with self._connection as connection:
            return connection.execute(
                'select url, date_saved from links where link_id = ?',
                (a_link_id,)
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

    def get_ids_of_links_with_tag(self, a_tag):
        with self._connection as connection:
            list_of_rows = connection.execute(
                'select link_id from tags where name = ?',
                (a_tag,)
            ).fetchall()

            return (link_id for (link_id,) in list_of_rows)

    def get_tags_of_link_with_id(self, a_link_id):
        with self._connection as connection:
            list_of_rows = connection.execute(
                'select name from tags where link_id = ?',
                (a_link_id,)
            ).fetchall()

            return tuple(tag for (tag,) in list_of_rows)


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
