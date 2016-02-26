from expects import expect, contain

from ..fixtures import one_link
from ..helpers import an_in_memory_sqlite_linkstore


with description('changing tags'):
    with context('modifying tags'):
        with before.each:
            a_link = one_link()
            linkstore = an_in_memory_sqlite_linkstore()
            self.an_old_tag = a_link.tags[0]
            self.a_new_tag = 'a new tag'

            linkstore.save(a_link)

            linkstore.modify_tag(a_link, {self.an_old_tag: self.a_new_tag})

            self.modified_link = linkstore.get_all()[0]

        with it('adds a new tag'):
            expect(self.modified_link.tags).to(contain(self.a_new_tag))

        with it('removes the old tag'):
            expect(self.modified_link.tags).not_to(contain(self.an_old_tag))
