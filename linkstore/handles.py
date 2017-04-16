from .links import SqliteTable


class Handles(object):
    def __init__(self, handles_table):
        self._handles_table = handles_table

    def compute_for(self, url):
        return self._handles_table.get_or_compute_handle_for(url)

    def retrieve_url_from(self, handle):
        return self._handles_table.get_url_from(handle)


class HandlesTable(SqliteTable):
    SQL_COMMAND_FOR_TABLE_CREATION = '''
        create table if not exists handles(
            handle
                integer primary key autoincrement,
            url
                unique
                not null
        )
    '''

    def get_or_compute_handle_for(self, url):
        with self._connection as connection:
            connection.execute(
                'insert or ignore into handles(url) values(?)',
                (url,)
            )

            row = connection.execute(
                'select handle from handles where url = ?',
                (url,)
            ).fetchone()
            handle = row[0]

            return handle

    def get_url_from(self, handle):
        with self._connection as connection:
            row = connection.execute(
                'select url from handles where handle = ?',
                (handle,)
            ).fetchone()
            url = row[0]

            return url
