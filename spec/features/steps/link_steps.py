from expects import expect, be_true

from linkstore.linkstore import Linkstore
from linkstore.link_storage import LinkStorage

link_storage = LinkStorage()
linkstore = Linkstore(link_storage)

@given(u'an URL and a tag')
def save_url_and_tag(context):
    context.an_url = 'https://www.example.com/'
    context.a_tag = 'favourites'

@when(u'I request that they be saved')
def perform_save(context):
    linkstore.save_link(context.an_url, context.a_tag)

@then(u'they should be successfully saved')
def verify_link_was_saved(context):
    all_links = link_storage.get_all()

    expect(any(
        map(
            lambda link: link == (context.an_url, context.a_tag),
            all_links
        )
    )).to(be_true)
