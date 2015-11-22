from expects import expect, equal, raise_error
from doublex import Stub, Spy
from doublex_expects import have_been_called, have_been_called_with

from linkstore.link_storage import SqliteLinkStorage, AutoclosingSqliteConnection


with description('the SQLite link storage'):
    with context('when saving links'):
        with it('can be given a single tag'):
            link_storage = SqliteLinkStorage(in_memory=True)
            an_url = 'an url'
            a_tag = 'favourites'

            expect(lambda: link_storage.save(an_url, a_tag)).not_to(raise_error)

        with it('can be given a tuple of tags'):
            link_storage = SqliteLinkStorage(in_memory=True)
            an_url = 'an url'
            some_tags = ('favourites', 'starred', 'unmissables')

            expect(lambda: link_storage.save(an_url, some_tags)).not_to(raise_error)

    with context('when retrieving links by tag'):
        with before.each:
            self.a_tag = 'favourites'
            self.link_storage = SqliteLinkStorage(in_memory=True)
            self.urls_to_save = [ 'an url', 'another url', 'yet another one' ]

        with it('returns all the links saved with that tag'):
            for url in self.urls_to_save:
                self.link_storage.save(url, self.a_tag)

            expect(self.link_storage.find_by_tag(self.a_tag)).to(
                equal([ (url, (self.a_tag,)) for url in self.urls_to_save ])
            )

        with it('doesn\'t return links which weren\'t saved with that tag'):
            for url in self.urls_to_save:
                self.link_storage.save(url, self.a_tag)

            url_of_link_with_different_tag = 'one more url'
            self.link_storage.save(url_of_link_with_different_tag, 'a different tag')

            for link in self.link_storage.find_by_tag(self.a_tag):
                expect(link[0]).not_to(equal(url_of_link_with_different_tag))

        with it('returns all the links saved with at least that tag'):
            another_tag = 'another tag'
            for url in self.urls_to_save:
                self.link_storage.save(url, (self.a_tag, another_tag))

            expect(self.link_storage.find_by_tag(self.a_tag)).to(
                equal([ (url, (self.a_tag, another_tag)) for url in self.urls_to_save ])
            )

    with context('when retrieving all links'):
        with it('returns all links previously saved'):
            link_storage = SqliteLinkStorage(in_memory=True)
            links_to_save = [
                ('an url', ('a tag',)),
                ('another url', ('another tag',)),
                ('one more url', ('a different tag',)),
                ('and one more', ('with one tag', 'and another tag'))
            ]

            for link in links_to_save:
                link_storage.save(*link)
            all_saved_links = links_to_save

            all_retrieved_links = link_storage.get_all()
            expect(all_retrieved_links).to(equal(all_saved_links))


    with description('the autoclosing SQLite connection'):
        with context('when used as a context manager'):
            with it('closes the connection after the with block is executed'):
                sqlite_connection = Spy()
                with Stub() as sqlite_connection_provider_stub:
                    sqlite_connection_provider_stub.get().returns(sqlite_connection)

                with AutoclosingSqliteConnection(sqlite_connection_provider_stub):
                    expect(sqlite_connection.close).not_to(have_been_called)

                expect(sqlite_connection.close).to(have_been_called_with().once)
