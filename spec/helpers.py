from expects import have_length, contain
from doublex import Stub

from linkstore.link_storage import SqliteLinkStorage, SqliteConnectionFactory
from linkstore.clock import Clock


def an_in_memory_sqlite_link_storage_on_any_date():
    return an_in_memory_sqlite_link_storage_on_date('18/12/2015')

def an_in_memory_sqlite_link_storage_on_date(a_date):
    return an_in_memory_sqlite_link_storage_with_clock(stubbed_clock_on_date(a_date))

def stubbed_clock_on_date(a_date):
    with Stub(Clock) as clock_stub:
        clock_stub.date_of_today().returns(a_date)

    return clock_stub

def an_in_memory_sqlite_link_storage_with_clock(a_clock):
    return SqliteLinkStorage(
        SqliteConnectionFactory.create_in_memory(),
        a_clock
    )

def have_the_same_length_as(expected):
    return have_length(len(expected))

def tuple_containing(*values):
    return contain(*values)
