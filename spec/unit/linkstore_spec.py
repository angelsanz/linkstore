from expects import expect, be_none
from doublex import Spy
from doublex_expects import have_been_called_with

from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteLinkStorage


with description('the link store'):
    with context('when adding a link'):
        with before.each:
            self.an_url = 'https://www.example.com/'

            self.link_storage_spy = Spy(SqliteLinkStorage)
            self.linkstore = Linkstore(self.link_storage_spy)

        with context('with one tag'):
            with before.each:
                self.a_tag = 'favourites'

            with it('delegates to the storage'):
                self.linkstore.save_link(self.an_url, self.a_tag)

                expect(self.link_storage_spy.save).to(
                    have_been_called_with(self.an_url, self.a_tag).once
                )

            with it('returns nothing'):
                return_value = self.linkstore.save_link(self.an_url, self.a_tag)

                expect(return_value).to(be_none)

        with context('with more than one tag'):
            with before.each:
                self.some_tags = ('favourites', 'must-see', 'whatever')

            with it('delegates to the storage'):
                self.linkstore.save_link(self.an_url, self.some_tags)

                expect(self.link_storage_spy.save).to(
                    have_been_called_with(self.an_url, self.some_tags).once
                )

            with it('returns nothing'):
                return_value = self.linkstore.save_link(self.an_url, self.some_tags)

                expect(return_value).to(be_none)


    with context('when retrieving links by tag'):
        with it('delegates to the storage'):
            a_tag = 'favourites'
            link_storage_spy = Spy(SqliteLinkStorage)
            linkstore = Linkstore(link_storage_spy)

            linkstore.find_by_tag(a_tag)

            expect(link_storage_spy.find_by_tag).to(
                have_been_called_with(a_tag).once
            )

    with context('when retrieving all links'):
        with it('delegates to the storage'):
            link_storage_spy = Spy(SqliteLinkStorage)
            linkstore = Linkstore(link_storage_spy)

            linkstore.get_all()

            expect(link_storage_spy.get_all).to(
                have_been_called_with().once
            )
