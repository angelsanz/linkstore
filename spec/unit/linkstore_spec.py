from expects import expect, be_none
from doublex import Spy
from doublex_expects import have_been_called_with

from linkstore.linkstore import Linkstore
from linkstore.link_storage import LinkStorage

with description('the linkstore object'):
    with context('when adding a link'):
        with it('delegates to the storage and returns nothing'):
            an_url = 'https://www.example.com/'
            a_tag = 'favourites'

            link_storage_spy = Spy(LinkStorage)
            linkstore = Linkstore(link_storage_spy)

            expect(linkstore.save_link(an_url, a_tag)).to(be_none)
            expect(link_storage_spy.save).to(have_been_called_with(an_url, a_tag).once)
