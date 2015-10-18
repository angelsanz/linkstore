from expects import expect, contain


@given(u'an URL and a tag')
def save_url_and_tag(context):
    context.an_url = 'https://www.example.com/'
    context.a_tag = 'favourites'

@when(u'I request that they be saved')
def perform_save(context):
    context.linkstore.save_link(context.an_url, context.a_tag)

@then(u'they should be successfully saved')
def verify_link_was_saved(context):
    all_links = context.link_storage.get_all()
    expect(all_links).to(contain((context.an_url, context.a_tag)))


@given(u'I have saved a link with tag "{given_tag}"')
def save_link_with_given_tag(context, given_tag):
    context.an_url = 'https://www.example.com/'
    context.given_tag = given_tag

    context.linkstore.save_link(context.an_url, context.given_tag)

@when(u'I retrieve all links with tag "{given_tag}"')
def retrieve_all_links_with_given_tag(context, given_tag):
    context.all_links_with_given_tag = context.linkstore.find_by_tag(given_tag)

@then(u'I should get that link\'s URL')
def verify_saved_link_is_present(context):
    expect(context.all_links_with_given_tag).to(
        contain((context.an_url, context.given_tag))
    )
