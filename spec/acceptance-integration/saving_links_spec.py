from expects import expect, contain

from ..helpers import an_in_memory_sqlite_linkstore
from ..fixtures import one_link


with description('saving a link'):
    with it('is successfully saved'):
        a_link = one_link()
        linkstore = an_in_memory_sqlite_linkstore()

        linkstore.save(a_link)

        expect(linkstore.get_all()).to(contain(a_link))
