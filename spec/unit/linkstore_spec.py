from expects import expect, be_none
from doublex import Spy, Stub
from doublex_expects import have_been_called_with

from linkstore.link import Link
from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteLinkStorage

from ..fixtures import data_for_some_links


with description('the link store'):
    with before.each:
        self.link_storage_spy = Spy(SqliteLinkStorage)
        self.link_creator_spy = Spy().link_creator_spy
        self.linkstore = Linkstore(self.link_storage_spy, self.link_creator_spy)

    with context('when adding a link'):
        with before.each:
            self.a_link = Stub(Link)

        with it('delegates to the storage'):
            self.linkstore.save(self.a_link)

            expect(self.link_storage_spy.save).to(
                have_been_called_with(self.a_link).once
            )

        with it('returns nothing'):
            return_value = self.linkstore.save(self.a_link)

            expect(return_value).to(be_none)


    with context('when retrieving links'):
        with context('by tag'):
            with before.each:
                self.a_tag = 'favourites'
                with self.link_storage_spy:
                    self.link_storage_spy.find_by_tag(self.a_tag).returns(data_for_some_links())

            with it('delegates to the storage'):
                self.linkstore.find_by_tag(self.a_tag)

                expect(self.link_storage_spy.find_by_tag).to(
                    have_been_called_with(self.a_tag).once
                )

            with it('calls the creator once per record returned by the storage'):
                self.linkstore.find_by_tag(self.a_tag)

                for link_record in data_for_some_links():
                    expect(self.link_creator_spy).to(have_been_called_with(link_record).once)

        with context('all links'):
            with before.each:
                with self.link_storage_spy:
                    self.link_storage_spy.get_all().returns(data_for_some_links())

            with it('delegates to the storage'):
                self.linkstore.get_all()

                expect(self.link_storage_spy.get_all).to(
                    have_been_called_with().once
                )

            with it('calls the creator once per record returned by the storage'):
                self.linkstore.get_all()

                for link_record in data_for_some_links():
                    expect(self.link_creator_spy).to(have_been_called_with(link_record).once)
