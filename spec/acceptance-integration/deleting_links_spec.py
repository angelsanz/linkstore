from expects import expect, contain

from ..helpers import an_in_memory_sqlite_linkstore
from ..fixtures import one_link


with description('deleting previously saved links'):
    with it('is successfully deleted'):
        a_link = one_link()
        linkstore = an_in_memory_sqlite_linkstore()
        linkstore.save(a_link)

        linkstore.delete(a_link)

        expect(linkstore.get_all()).not_to(contain(a_link))
