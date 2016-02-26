import sqlite3

from linkstore.link import Link
from linkstore.link_storage import SqliteLinkStorage, AutoclosingSqliteConnection, LinksTable, TagsTable

from expects import expect, equal
from doublex import Stub, Spy, Mock
from doublex_expects import have_been_called, have_been_called_with, have_been_satisfied_in_any_order, anything

from ..helpers import an_in_memory_sqlite_link_storage
from ..fixtures import some_stubbed_links, LinkStub, some_stubbed_links_with_tags, a_tag_modification


with description('the SQLite link storage'):
    with before.each:
        self.link_storage = an_in_memory_sqlite_link_storage()

    with context('when saving links'):
        with it('''reads the link's attributes'''):
            with Mock(Link) as link_mock:
                link_mock.url.returns('an url')
                link_mock.url.returns('an url')
                link_mock.tags.returns(('a tag', 'another tag'))
                link_mock.date.returns('a date')

            self.link_storage.save(link_mock)

            expect(link_mock).to(have_been_satisfied_in_any_order)

    with context('when retrieving links by tag'):
        with before.each:
            self.a_tag = 'favourites'

        with it('returns all the links saved with that tag'):
            links_to_save = some_stubbed_links_with_tags((self.a_tag,))
            for link_stub in links_to_save:
                self.link_storage.save(link_stub)
            saved_links = links_to_save


            expect(self.link_storage.find_by_tag(self.a_tag)).to(
                equal([
                    (link_stub.url, link_stub.tags, link_stub.date)
                    for link_stub in saved_links
                ])
            )

        with it('''doesn't return links which weren't saved with that tag'''):
            for link_stub in some_stubbed_links_with_tags((self.a_tag,)):
                self.link_storage.save(link_stub)

            url_of_link_with_different_tag = 'the url of a link with a different tag'
            self.link_storage.save(LinkStub(url_of_link_with_different_tag, ('a different tag',), 'irrelevant date'))

            for link_record in self.link_storage.find_by_tag(self.a_tag):
                expect(link_record[0]).not_to(equal(url_of_link_with_different_tag))

        with it('returns all the links saved with at least that tag'):
            another_tag = 'another tag'
            links_to_save = some_stubbed_links_with_tags((self.a_tag, another_tag))
            for link_stub in links_to_save:
                self.link_storage.save(link_stub)
            saved_links = links_to_save


            expect(self.link_storage.find_by_tag(self.a_tag)).to(
                equal([
                    (link_stub.url, link_stub.tags, link_stub.date)
                    for link_stub in saved_links
                ])
            )

    with context('when retrieving all links'):
        with it('returns all previously saved links'):
            links_to_save = some_stubbed_links()
            for link_stub in links_to_save:
                self.link_storage.save(link_stub)
            saved_links = links_to_save

            expect(self.link_storage.get_all()).to(
                equal([
                    (link_stub.url, link_stub.tags, link_stub.date)
                    for link_stub in saved_links
                ])
            )

    with context('when replacing a tag of a link'):
        with before.each:
            self.tags_table_spy = Spy(TagsTable)
            links_table_dummy = Stub(LinksTable)
            self.link_storage = SqliteLinkStorage({'links': links_table_dummy, 'tags': self.tags_table_spy})

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


with description('the autoclosing SQLite connection'):
    with context('when used as a context manager'):
        with it('closes the connection after the `with` block is executed'):
            sqlite_connection = Spy(sqlite3.Connection)
            with Stub() as sqlite_connection_provider_stub:
                sqlite_connection_provider_stub.get().returns(sqlite_connection)

            with AutoclosingSqliteConnection(sqlite_connection_provider_stub):
                expect(sqlite_connection.close).not_to(have_been_called)

            expect(sqlite_connection.close).to(have_been_called_with().once)
