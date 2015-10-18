from expects import expect, equal

from linkstore.link_storage import InMemoryLinkStorage, SqliteLinkStorage


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
