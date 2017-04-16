from expects import expect, be_an, equal

from linkstore import factory


with description('Handles'):
    with it('can be computed for any url'):
        handles = factory.create_handles()
        an_url = 'an url'

        handle = handles.compute_for(an_url)

        expect(handle).to(be_an(int))

    with it('does not change for each url'):
        handles = factory.create_handles()
        an_url = 'an url'

        old_handle = handles.compute_for(an_url)
        new_handle = handles.compute_for(an_url)

        expect(old_handle).to(equal(new_handle))

    with it('is different for different urls'):
        handles = factory.create_handles()
        an_url = 'an url'
        another_url = 'another url'

        a_handle = handles.compute_for(an_url)
        another_handle = handles.compute_for(another_url)

        expect(a_handle).not_to(equal(another_handle))

    with it('can be retrieved by the url for which they were computed'):
        handles = factory.create_handles()
        an_url = 'an url'
        handle = handles.compute_for(an_url)

        url = handles.retrieve_url_from(handle)

        expect(url).to(equal(an_url))
