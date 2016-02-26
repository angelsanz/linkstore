from expects import expect, equal

from linkstore.link import Link

from ..helpers import an_in_memory_sqlite_linkstore
from ..fixtures import some_links_with_tags, some_links


with description('retrieving links'):
    with before.each:
        self.linkstore = an_in_memory_sqlite_linkstore()

    with context('by one tag'):
        with it('returns the links originally saved with the target tag'):
            a_tag = 'the target tag'
            some_links_with_target_tag = some_links_with_tags((a_tag,))

            for link in some_links_with_target_tag:
                self.linkstore.save(link)

            all_links_with_target_tag = self.linkstore.find_by_tag(a_tag)
            expect(all_links_with_target_tag).to(equal(some_links_with_target_tag))

        with it('returns links originally saved with the target tag and some other tags'):
            a_tag = 'the target tag'
            some_links_with_target_tag_and_others = some_links_with_tags((a_tag, 'some other tag', 'yet some other tag'))

            for link in some_links_with_target_tag_and_others:
                self.linkstore.save(link)

            all_links_with_target_tag = self.linkstore.find_by_tag(a_tag)
            expect(all_links_with_target_tag).to(equal(some_links_with_target_tag_and_others))

        with it('''doesn't return links which weren't saved with the target tag'''):
            a_tag = 'the target tag'
            some_links_with_target_tag = some_links_with_tags((a_tag,))
            for link in some_links_with_target_tag:
                self.linkstore.save(link)
            a_different_link = Link('a different url', 'not the target tag', 'whatever date')

            self.linkstore.save(a_different_link)

            for link in self.linkstore.find_by_tag(a_tag):
                expect(link).not_to(equal(a_different_link))

    with context('all links'):
        with it('returns all links'):
            links_to_save = some_links()

            for link in links_to_save:
                self.linkstore.save(link)
            saved_links = links_to_save

            expect(self.linkstore.get_all()).to(equal(saved_links))
