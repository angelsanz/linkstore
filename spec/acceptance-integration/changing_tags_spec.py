from expects import expect, contain

from ..fixtures import one_link, some_links_with_at_lesat_the_tags
from ..helpers import an_in_memory_sqlite_linkstore


with description('changing tags'):
    with before.each:
        self.a_link = one_link()
        self.linkstore = an_in_memory_sqlite_linkstore()
        self.a_new_tag = 'a new tag'

    with context('modifying tags for one link'):
        with before.each:
            self.linkstore.save(self.a_link)

            self.one_of_the_orignal_tags = self.a_link.tags[0]
            self.linkstore.modify_tag(self.a_link, {self.one_of_the_orignal_tags: self.a_new_tag})

            self.modified_link = self.linkstore.get_all()[0]

        with it('adds the new tag'):
            expect(self.modified_link.tags).to(contain(self.a_new_tag))

        with it('removes the old tag'):
            expect(self.modified_link.tags).not_to(contain(self.one_of_the_orignal_tags))

    with context('modifying tags for all links'):
        with before.each:
            self.one_of_the_orignal_tags = 'the original tag'

            for link in some_links_with_at_lesat_the_tags((self.one_of_the_orignal_tags,)):
                self.linkstore.save(link)

            self.linkstore.modify_tag_globally({self.one_of_the_orignal_tags: self.a_new_tag})

        with it('adds the new tag'):
            for modified_link in self.linkstore.get_all():
                expect(modified_link.tags).to(contain(self.a_new_tag))

        with it('removes the old tag'):
            for modified_link in self.linkstore.get_all():
                expect(modified_link.tags).not_to(contain(self.one_of_the_orignal_tags))

    with context('adding tags'):
        with before.each:
            self.linkstore.save(self.a_link)

            self.some_new_tags = (self.a_new_tag, 'another new tag', 'one more new tag')
            self.linkstore.add_tags(self.a_link, self.some_new_tags)

            self.modified_link = self.linkstore.get_all()[0]

        with it('preserves the original tags'):
            for original_tag in self.a_link.tags:
                expect(self.modified_link.tags).to(contain(original_tag))

        with it('adds the new tags'):
            for tag in self.some_new_tags:
                expect(self.modified_link.tags).to(contain(tag))
