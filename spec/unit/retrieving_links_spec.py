from expects import expect, equal, have_length

from linkstore import factory

from ..fixtures import some_links_with_tags, some_links


with description('retrieving links'):
    with before.each:
        self.links_service = factory.create_links_service()

    with context('by one tag'):
        with it('returns links saved with the target tag'):
            target_tag = 'the target tag'
            some_links_with_target_tag = some_links_with_tags((target_tag, 'some other tag', 'yet some other tag'))
            for url, tags, date in some_links_with_target_tag:
                self.links_service.save_link(url, tags, date)

            links_with_target_tag = self.links_service.retrieve_links_by_tag(target_tag)

            expect(links_with_target_tag).to(have_length(len(some_links_with_target_tag)))

        with it('''doesn't return links which weren't saved with the target tag'''):
            target_tag = 'the target tag'
            some_links_with_target_tag = some_links_with_tags((target_tag,))
            for url, tags, date in some_links_with_target_tag:
                self.links_service.save_link(url, tags, date)
            a_different_url = 'a different url'
            a_different_tag = 'not the target tag'
            self.links_service.save_link(a_different_url, (a_different_tag,), 'whatever date')

            links_with_target_tag = self.links_service.retrieve_links_by_tag(target_tag)

            for link in links_with_target_tag:
                expect(link.url).not_to(equal(a_different_url))

    with context('all links'):
        with it('returns all links'):
            links_to_save = some_links()

            for url, tags, date in links_to_save:
                self.links_service.save_link(url, tags, date)
            saved_links = links_to_save

            expect(self.links_service.get_all()).to(have_length(len(saved_links)))
