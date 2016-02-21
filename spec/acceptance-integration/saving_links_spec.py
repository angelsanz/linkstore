from expects import expect, contain

from linkstore.linkstore import Linkstore

from ..helpers import an_in_memory_sqlite_link_storage_on_any_date, tuple_containing


with description('saving a link'):
    with before.each:
        self.an_url = 'https://www.example.com/'
        self.linkstore = Linkstore(an_in_memory_sqlite_link_storage_on_any_date())

    with context('with one tag'):
        with it('is successfully saved'):
            a_tag = 'favourites'

            self.linkstore.save_link(self.an_url, a_tag)

            all_links = self.linkstore.get_all()
            expect(all_links).to(
                contain(tuple_containing(self.an_url, (a_tag,)))
            )

    with context('with more than one tag'):
        with it('is successfully saved'):
            some_tags = ('favourites', 'misc')

            self.linkstore.save_link(self.an_url, some_tags)

            all_links = self.linkstore.get_all()
            expect(all_links).to(
                contain(tuple_containing(self.an_url, some_tags))
            )
