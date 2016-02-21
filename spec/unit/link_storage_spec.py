import sqlite3

from linkstore.link_storage import AutoclosingSqliteConnection
from linkstore.clock import Clock

from expects import expect, equal, raise_error
from doublex import Stub, Spy
from doublex_expects import have_been_called, have_been_called_with

from ..helpers import (
    an_in_memory_sqlite_link_storage_on_date,
    an_in_memory_sqlite_link_storage_on_any_date,
    an_in_memory_sqlite_link_storage_with_clock
)


with description('the SQLite link storage'):
    with context('when saving links'):
        with before.each:
            self.an_url = 'an url'

        with it('can be given a single tag'):
            a_tag = 'favourites'
            link_storage = an_in_memory_sqlite_link_storage_on_any_date()

            expect(lambda: link_storage.save(self.an_url, a_tag)).not_to(raise_error)

        with it('can be given a tuple of tags'):
            some_tags = ('favourites', 'starred', 'unmissables')
            link_storage = an_in_memory_sqlite_link_storage_on_any_date()

            expect(lambda: link_storage.save(self.an_url, some_tags)).not_to(raise_error)

        with it('delegates to the clock in order to get the current date'):
            a_tag = 'favourites'
            with Spy(Clock) as clock_spy:
                clock_spy.date_of_today().returns('any date whatsoever')
            link_storage = an_in_memory_sqlite_link_storage_with_clock(clock_spy)

            link_storage.save(self.an_url, a_tag)

            expect(clock_spy.date_of_today).to(have_been_called_with().once)

    with context('when retrieving links by tag'):
        with before.each:
            self.a_tag = 'favourites'
            self.urls_to_save = [ 'an url', 'another url', 'yet another one' ]
            self.a_date = '18/12/2015'

            self.link_storage = an_in_memory_sqlite_link_storage_on_date(self.a_date)

        with it('returns all the links saved with that tag'):
            for url in self.urls_to_save:
                self.link_storage.save(url, self.a_tag)

            expect(self.link_storage.find_by_tag(self.a_tag)).to(
                equal([ (url, self.a_date, (self.a_tag,)) for url in self.urls_to_save ])
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
                equal([ (url, self.a_date, (self.a_tag, another_tag)) for url in self.urls_to_save ])
            )

    with context('when retrieving all links'):
        with it('returns all previously saved links'):
            a_date = '18/12/2015'
            link_storage = an_in_memory_sqlite_link_storage_on_date(a_date)

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
            expect(all_retrieved_links).to(
                equal([ (url, a_date, tags) for url, tags in all_saved_links ])
            )


    with description('the autoclosing SQLite connection'):
        with context('when used as a context manager'):
            with it('closes the connection after the with block is executed'):
                sqlite_connection = Spy(sqlite3.Connection)
                with Stub() as sqlite_connection_provider_stub:
                    sqlite_connection_provider_stub.get().returns(sqlite_connection)

                with AutoclosingSqliteConnection(sqlite_connection_provider_stub):
                    expect(sqlite_connection.close).not_to(have_been_called)

                expect(sqlite_connection.close).to(have_been_called_with().once)
