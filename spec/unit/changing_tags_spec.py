from expects import expect, contain

from linkstore import factory

from ..fixtures import some_links_with_at_lesat_the_tags


with description('changing tags'):
    with before.each:
        self.an_url = 'an_url'
        self.a_tag_to_change = 'a tag to change'
        self.some_tags = (self.a_tag_to_change, 'another tag')
        self.a_date = 'a date'

        self.links_service = factory.create_links_service()
        self.a_new_tag = 'a new tag'

    with context('modifying tags for one link'):
        with before.each:
            self.links_service.save_link(self.an_url, self.some_tags, self.a_date)

            self.links_service.modify_tag_of_link_with_url(self.an_url, {self.a_tag_to_change: self.a_new_tag})

            self.modified_link = self.links_service.get_all()[0]

        with it('adds the new tag'):
            expect(self.modified_link.tags).to(contain(self.a_new_tag))

        with it('removes the old tag'):
            expect(self.modified_link.tags).not_to(contain(self.a_tag_to_change))

    with context('modifying tags for all links'):
        with before.each:
            self.a_tag_to_change = 'the original tag'

            for url, tags, date in some_links_with_at_lesat_the_tags((self.a_tag_to_change,)):
                self.links_service.save_link(url, tags, date)

            self.links_service.modify_tag_of_all_links({self.a_tag_to_change: self.a_new_tag})

        with it('adds the new tag'):
            for modified_link in self.links_service.get_all():
                expect(modified_link.tags).to(contain(self.a_new_tag))

        with it('removes the old tag'):
            for modified_link in self.links_service.get_all():
                expect(modified_link.tags).not_to(contain(self.a_tag_to_change))

    with context('adding tags'):
        with before.each:
            self.links_service.save_link(self.an_url, self.some_tags, self.a_date)

            self.some_new_tags = (self.a_new_tag, 'another new tag', 'one more new tag')
            self.links_service.add_tags_to_link_with_url(self.an_url, self.some_new_tags)

            self.modified_link = self.links_service.get_all()[0]

        with it('preserves the original tags'):
            for original_tag in self.some_tags:
                expect(self.modified_link.tags).to(contain(original_tag))

        with it('adds the new tags'):
            for new_tag in self.some_new_tags:
                expect(self.modified_link.tags).to(contain(new_tag))
