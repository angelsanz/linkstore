from expects import expect, equal

from ..helpers import an_in_memory_sqlite_linkstore
from ..fixtures import some_links, one_link


with description('retrieving links'):
    with before.each:
        self.linkstore = an_in_memory_sqlite_linkstore()

    with description('by one tag'):
        with it('returns the URL and the date when the links were saved'):
            a_link = one_link()

            self.linkstore.save(a_link)

            all_links_with_given_tag = self.linkstore.find_by_tag(a_link.tags[0])
            expect(all_links_with_given_tag).to(equal([a_link]))

    with description('without a tag'):
        with it('returns all links'):
            links_to_save = some_links()

            for link in links_to_save:
                self.linkstore.save(link)
            saved_links = links_to_save

            all_links = self.linkstore.get_all()
            expect(all_links).to(equal(saved_links))
