from expects import expect, contain

from linkstore.linkstore import Linkstore

from ..helpers import an_in_memory_sqlite_link_storage_on_any_date, tuple_containing


with description('saving a link'):
    with before.each:
        self.link_storage = an_in_memory_sqlite_link_storage_on_any_date()
        self.linkstore = Linkstore(self.link_storage)

    with context('with one tag'):
        with it('is successfully saved'):
            an_url = 'https://www.example.com/'
            a_tag = 'favourites'

            self.linkstore.save_link(an_url, a_tag)

            all_links = self.link_storage.get_all()
            expect(all_links).to(
                contain(tuple_containing(an_url, (a_tag,)))
            )

    with context('with more than one tag'):
        with it('is successfully saved'):
            an_url = 'https://www.example.com/'
            some_tags = ('favourites', 'misc')

            self.linkstore.save_link(an_url, some_tags)

            all_links = self.link_storage.get_all()
            expect(all_links).to(
                contain(tuple_containing(an_url, some_tags))
            )
