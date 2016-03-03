from expects import expect, contain

from ..fixtures import one_link
from ..helpers import an_in_memory_sqlite_linkstore


with description('changing tags'):
    with before.each:
        self.a_link = one_link()
        self.linkstore = an_in_memory_sqlite_linkstore()
        self.one_of_the_orignal_tags = self.a_link.tags[0]
        self.a_new_tag = 'a new tag'

        self.linkstore.save(self.a_link)

    with context('modifying tags'):
        with before.each:
            self.linkstore.modify_tag(self.a_link, {self.one_of_the_orignal_tags: self.a_new_tag})
            self.modified_link = self.linkstore.get_all()[0]

        with it('adds a new tag'):
            expect(self.modified_link.tags).to(contain(self.a_new_tag))

        with it('removes the old tag'):
            expect(self.modified_link.tags).not_to(contain(self.one_of_the_orignal_tags))

    with context('adding tags'):
        with before.each:
            self.linkstore.add_tag(self.a_link, self.a_new_tag)
            self.the_link = self.linkstore.get_all()[0]

        with it('preserves the original tag'):
            expect(self.the_link.tags).to(contain(self.one_of_the_orignal_tags))

        with it('adds the new tag'):
            expect(self.the_link.tags).to(contain(self.a_new_tag))
