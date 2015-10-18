from expects import expect, equal
from doublex import Spy
from doublex_expects import have_been_called, have_been_called_with

from linkstore.link_storage import InMemoryLinkStorage, SqliteLinkStorage, AutoclosingSqliteConnection


with description('the in-memory link storage'):
    with context('when retrieving links by tag'):
        with before.each:
            self.a_tag = 'favourites'
            self.link_storage = InMemoryLinkStorage()
            self.urls_to_save = [ 'an url', 'another url', 'yet another one' ]

        with it('returns all the links saved with that tag'):
            for url in self.urls_to_save:
                self.link_storage.save(url, self.a_tag)

            expect(self.link_storage.find_by_tag(self.a_tag)).to(
                equal([ (url, self.a_tag) for url in self.urls_to_save ])
            )

        with it('doesn\'t return links which were saved with another tag'):
            for url in self.urls_to_save:
                self.link_storage.save(url, self.a_tag)

            url_of_link_with_different_tag = 'one more url'
            self.link_storage.save(url_of_link_with_different_tag, 'a different tag')

            for link in self.link_storage.find_by_tag(self.a_tag):
                expect(link[0]).not_to(equal(url_of_link_with_different_tag))


with description('the SQLite link storage'):
    with context('when retrieving links by tag'):
        with before.each:
            self.a_tag = 'favourites'
            self.link_storage = SqliteLinkStorage(in_memory=True)
            self.urls_to_save = [ 'an url', 'another url', 'yet another one' ]

        with it('returns all the links saved with that tag'):
            for url in self.urls_to_save:
                self.link_storage.save(url, self.a_tag)

            expect(self.link_storage.find_by_tag(self.a_tag)).to(
                equal([ (url, self.a_tag) for url in self.urls_to_save ])
            )

        with it('doesn\'t return links which were saved with another tag'):
            for url in self.urls_to_save:
                self.link_storage.save(url, self.a_tag)

            url_of_link_with_different_tag = 'one more url'
            self.link_storage.save(url_of_link_with_different_tag, 'a different tag')

            for link in self.link_storage.find_by_tag(self.a_tag):
                expect(link[0]).not_to(equal(url_of_link_with_different_tag))

    with context('when retrieving all links'):
        with it('returns all links previously saved'):
            link_storage = SqliteLinkStorage(in_memory=True)
            links_to_save = [
                ('an url', 'a tag'),
                ('another url', 'another tag'),
                ('one more url', 'a different tag')
            ]

            for link in links_to_save:
                link_storage.save(*link)

            all_saved_links = links_to_save


            all_retrieved_links = link_storage.get_all()


            expect(all_retrieved_links).to(equal(all_saved_links))


    with description('the autoclosing connection class'):
        with context('when used as a context manager'):
            with it('closes the connection after the with block is executed'):
                autoclosing_connection = AutoclosingSqliteConnection()
                connection = Spy()
                autoclosing_connection._create_new_connection = lambda: connection

                with autoclosing_connection:
                    expect(connection.close).not_to(have_been_called)

                expect(connection.close).to(have_been_called_with().once)
