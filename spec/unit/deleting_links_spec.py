from expects import expect, be_empty

from linkstore import factory


with description('deleting previously saved links'):
    with it('is successfully deleted'):
        an_url = 'an_url'
        some_tags = ('a_tag',)
        a_date = 'a date'
        links_service = factory.create_links_service()
        links_service.save_link(an_url, some_tags, a_date)

        links_service.delete_link_with_url(an_url)

        expect(links_service.get_all()).to(be_empty)
