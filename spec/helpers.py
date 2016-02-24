from expects import have_length

from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteLinkStorage, SqliteConnectionFactory
from linkstore.factory import create_link


def an_in_memory_sqlite_link_storage():
    return SqliteLinkStorage(SqliteConnectionFactory.create_in_memory())

def an_in_memory_sqlite_linkstore():
    return Linkstore(an_in_memory_sqlite_link_storage(), create_link)


def have_the_same_length_as(expected):
    return have_length(len(expected))
