from expects import expect, be_none
from doublex import Spy
from doublex_expects import have_been_called_with

from linkstore.linkstore import Linkstore
from linkstore.link_storage import InMemoryLinkStorage


with description('the link store'):
    with context('when adding a link'):
        with before.each:
            self.an_url = 'https://www.example.com/'
            self.a_tag = 'favourites'

            self.link_storage_spy = Spy(InMemoryLinkStorage)
            self.linkstore = Linkstore(self.link_storage_spy)

        with it('delegates to the storage'):
            self.linkstore.save_link(self.an_url, self.a_tag)

            expect(self.link_storage_spy.save).to(
                have_been_called_with(self.an_url, self.a_tag).once
            )

        with it('returns nothing'):
            return_value = self.linkstore.save_link(self.an_url, self.a_tag)

            expect(return_value).to(be_none)

    with context('when retrieving links by tag'):
        with it('delegates to the storage'):
            a_tag = 'favourites'
            link_storage_spy = Spy(InMemoryLinkStorage)
            linkstore = Linkstore(link_storage_spy)

            linkstore.find_by_tag(a_tag)

            expect(link_storage_spy.find_by_tag).to(
                have_been_called_with(a_tag).once
            )
