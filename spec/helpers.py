from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteConnectionFactory
from linkstore.factory import create_link, create_sqlite_link_storage_with_connection


def an_in_memory_sqlite_link_storage():
    return create_sqlite_link_storage_with_connection(SqliteConnectionFactory.create_in_memory())

def an_in_memory_sqlite_linkstore():
    return Linkstore(an_in_memory_sqlite_link_storage(), create_link)
