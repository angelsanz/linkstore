from doublex import Stub

from linkstore.clock import Clock
from linkstore.link_storage import SqliteLinkStorage


def an_in_memory_sqlite_link_storage_on_any_date():
    with Stub(Clock) as clock_dummy:
        clock_dummy.date_of_today().returns('18/12/2015')

    return SqliteLinkStorage(clock_dummy, in_memory=True)

def an_in_memory_sqlite_link_storage_on_date(a_date):
    with Stub(Clock) as clock_stub:
        clock_stub.date_of_today().returns(a_date)

    return SqliteLinkStorage(clock_stub, in_memory=True)
