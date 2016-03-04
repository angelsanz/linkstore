import sqlite3

from linkstore.link import Link
from linkstore.link_storage import SqliteLinkStorage, AutoclosingSqliteConnection, LinksTable, TagsTable

from expects import expect
from doublex import Stub, Spy, Mock
Dummy = Stub
from doublex_expects import have_been_called, have_been_called_with, have_been_satisfied_in_any_order, anything

from ..fixtures import a_tag_modification


with description('the SQLite link storage'):
    with context('when saving links'):
        with it('''reads the link's attributes'''):
            with Mock(Link) as link_mock:
                link_mock.url.returns('an url')
                link_mock.url.returns('an url')
                link_mock.tags.returns(('a tag', 'another tag'))
                link_mock.date.returns('a date')
            link_storage = SqliteLinkStorage({'links': Dummy(LinksTable), 'tags': Dummy(TagsTable)})

            link_storage.save(link_mock)

            expect(link_mock).to(have_been_satisfied_in_any_order)

    with context('when retrieving links by tag'):
        with it('asks the TagsTable for the ids of the links with the specified tag'):
            a_tag = 'favourites'
            with Spy(TagsTable) as tags_table_spy:
                tags_table_spy.get_ids_of_links_with_tag(a_tag).returns([])
            link_storage = SqliteLinkStorage({'links': Dummy(LinksTable), 'tags': tags_table_spy})

            link_storage.find_by_tag(a_tag)

            expect(tags_table_spy.get_ids_of_links_with_tag).to(
                have_been_called_with(a_tag).once
            )

    with context('when retrieving all links'):
        with it('asks the LinksTable for all its records'):
            with Spy(LinksTable) as links_table_spy:
                links_table_spy.get_all().returns([])
            link_storage = SqliteLinkStorage({'links': links_table_spy, 'tags': Dummy(TagsTable)})

            link_storage.get_all()

            expect(links_table_spy.get_all).to(
                have_been_called_with().once
            )

    with context('when replacing a tag of a link'):
        with before.each:
            self.tags_table_spy = Spy(TagsTable)
            self.link_storage = SqliteLinkStorage({'links': Dummy(LinksTable), 'tags': self.tags_table_spy})

        with context('when identifying the link with an url'):
            with it('asks the TagsTable to replace the tags'):
                an_url = 'an url'

                self.link_storage.replace_tag_in_link_with_url(an_url, a_tag_modification())

                expect(self.tags_table_spy.replace_tag_in_link_with_id).to(
                    have_been_called_with(anything, a_tag_modification()).once
                )

        with context('when identifying the link with an id'):
            with it('asks the TagsTable to replace the tags'):
                a_link_id = 32

                self.link_storage.replace_tag_in_link_with_id(a_link_id, a_tag_modification())

                expect(self.tags_table_spy.replace_tag_in_link_with_id).to(
                    have_been_called_with(a_link_id).once
                )

    with context('when adding a tag to a link'):
        with context('when identifying the link with an url'):
            with before.each:
                self.tags_table_spy = Spy(TagsTable)
                self.link_storage = SqliteLinkStorage({'links': Dummy(LinksTable), 'tags': self.tags_table_spy})

            with it('asks the TagsTable to add the tag'):
                an_url = 'an url'
                a_new_tag = 'a new tag'

                self.link_storage.add_tags_to_link_with_url(an_url, (a_new_tag,))

                expect(self.tags_table_spy.save_tags_for_link_with_id).to(
                    have_been_called_with(anything, (a_new_tag,)).once
                )


        with context('when identifying the link with an id'):
            with it('asks the TagsTable to add the tag'):
                a_link_id = 32
                a_new_tag = 'a new tag'

                self.link_storage.add_tags_to_link_with_id(a_link_id, (a_new_tag,))

                expect(self.tags_table_spy.save_tags_for_link_with_id).to(
                    have_been_called_with(a_link_id, (a_new_tag,)).once
                )


with description('the autoclosing SQLite connection'):
    with context('when used as a context manager'):
        with it('closes the connection after the `with` block is executed'):
            sqlite_connection = Spy(sqlite3.Connection)
            with Stub() as sqlite_connection_provider_stub:
                sqlite_connection_provider_stub.get().returns(sqlite_connection)

            with AutoclosingSqliteConnection(sqlite_connection_provider_stub):
                expect(sqlite_connection.close).not_to(have_been_called)

            expect(sqlite_connection.close).to(have_been_called_with().once)
