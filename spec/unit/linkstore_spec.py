from expects import expect, be_none
from doublex import Spy, Stub
from doublex_expects import have_been_called_with

from linkstore.link import Link
from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteLinkStorage

from ..fixtures import data_for_some_links, a_tag_modification


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
            with context('without ids'):
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

            with context('with ids'):
                with before.each:
                    with self.link_storage_spy:
                        self.link_storage_spy.get_all_with_ids().returns(data_for_some_links())

    with context('when modifying a tag of a link'):
        with context('when identifying the link with a Link object'):
            with it('delegates to the storage'):
                a_link = Stub(Link)

                self.linkstore.modify_tag(a_link, a_tag_modification())

                expect(self.link_storage_spy.replace_tag_in_link_with_url).to(
                    have_been_called_with(a_link.url, a_tag_modification()).once
                )

        with context('when identifying the link with its id'):
            with it('delegates to the storage'):
                a_link_id = 45

                self.linkstore.modify_tag_by_id(a_link_id, a_tag_modification())

                expect(self.link_storage_spy.replace_tag_in_link_with_id).to(
                    have_been_called_with(a_link_id).once
                )

    with context('when adding a tag to a link'):
        with context('when identifying the link with a Link object'):
            with it('delegates to the storage'):
                a_link = Stub(Link)
                a_new_tag = 'a new tag'

                self.linkstore.add_tag(a_link, a_new_tag)

                expect(self.link_storage_spy.add_tag_to_link_with_url).to(
                    have_been_called_with(a_link.url, a_new_tag).once
                )

        with context('when identifying the link with its id'):
            with it('delegates to the storage'):
                a_link_id = 45
                a_new_tag = 'a new tag'

                self.linkstore.add_tag_by_id(a_link_id, a_new_tag)

                expect(self.link_storage_spy.add_tag_to_link_with_id).to(
                    have_been_called_with(a_link_id, a_new_tag).once
                )
