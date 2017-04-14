from expects import expect, equal

from linkstore import factory


with description('saving a link'):
    with it('is successfully saved'):
        an_url = 'an_url'
        some_tags = ('a_tag',)
        a_date = 'a date'
        links_service = factory.create_links_service()

        links_service.save_link(an_url, some_tags, a_date)

        saved_link = links_service.get_all()[0]
        expect(saved_link.url).to(equal(an_url))
        expect(saved_link.tags).to(equal(some_tags))
        expect(saved_link.date).to(equal(a_date))
