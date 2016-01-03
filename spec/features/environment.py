from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteLinkStorage
from linkstore.clock import Clock

from doublex import Stub


def before_scenario(context, scenario):
    a_dummy_date = '18/12/2015'
    with Stub(Clock) as clock_dummy:
        clock_dummy.date_of_today().returns(a_dummy_date)

    context.link_storage = SqliteLinkStorage(clock_dummy, in_memory=True)
    context.linkstore = Linkstore(context.link_storage)
