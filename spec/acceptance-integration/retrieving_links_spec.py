from expects import expect, contain

from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteConnectionFactory, SqliteLinkStorage

from ..helpers import (
    an_in_memory_sqlite_link_storage_on_date,
    stubbed_clock_on_date,
    tuple_containing,
    have_the_same_length_as
)


with description('retrieving links'):
    with description('by one tag'):
        with it('returns the URL and the date when the links were saved'):
            an_url = 'https://www.example.com/'
            a_tag = 'favourites'
            a_date = '8/12/2015'
            linkstore = Linkstore(an_in_memory_sqlite_link_storage_on_date(a_date))

            linkstore.save_link(an_url, a_tag)

            all_links_with_given_tag = linkstore.find_by_tag(a_tag)
            expect(all_links_with_given_tag).to(
                contain(tuple_containing(an_url, a_date))
            )

    with description('without a tag'):
        with it('returns all links'):
            links_to_save = [
                ("https://www.example.com/",        ("favourites",), '12/03/2008'   ),
                ("https://www.another-example.net", ("misc",),       '35/56/89'     ),
                ("https://one-more.org",            ("extra",),      '789/23/677785')
            ]
            connection = SqliteConnectionFactory.create_in_memory()

            for link in links_to_save:
                linkstore = Linkstore(SqliteLinkStorage(connection, stubbed_clock_on_date(link[2])))
                linkstore.save_link(link[0], link[1])
            saved_links = links_to_save

            all_links = linkstore.get_all()
            expect(all_links).to(have_the_same_length_as(saved_links))

            for saved_link in saved_links:
                expect(all_links).to(
                    contain(tuple_containing(*saved_link))
                )
