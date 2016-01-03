from expects import expect, contain
from doublex import Mock

from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteLinkStorage
from linkstore.clock import Clock

from .helpers import tuple_containing


@given(u'the URL "{an_url}" and the tag "{a_tag}"')
def save_url_and_tag(context, an_url, a_tag):
    context.an_url = an_url
    context.a_tag = a_tag

@when(u'I request that they be saved')
def perform_save(context):
    context.linkstore.save_link(context.an_url, context.a_tag)

@then(u'they should be successfully saved')
def verify_link_was_saved(context):
    all_links = context.link_storage.get_all()
    expect(all_links).to(
        contain(tuple_containing(context.an_url, (context.a_tag,)))
    )

@given(u'the URL "{an_url}" and the tags "{a_tag}", "{another_tag}"')
def save_url_and_tags(context, an_url, a_tag, another_tag):
    context.an_url = an_url
    context.some_tags = (a_tag, another_tag)

@when(u'I request that the URL be saved with those tags')
def perform_save_with_both_tags(context):
    context.linkstore.save_link(context.an_url, context.some_tags)

@then(u'the URL should be saved with those tags')
def verify_link_was_saved_with_both_tags(context):
    all_links = context.link_storage.get_all()
    expect(all_links).to(
        contain(tuple_containing(context.an_url, context.some_tags))
    )




@given(u'I have saved the URL "{an_url}" with tag "{given_tag}"')
def save_link_with_given_tag(context, an_url, given_tag):
    context.a_date = "18/12/2015"
    with Mock(Clock) as clock_mock:
        clock_mock.date_of_today().returns(context.a_date)

    context.link_storage = SqliteLinkStorage(clock_mock, in_memory=True)
    context.linkstore = Linkstore(context.link_storage)
    context.an_url = an_url


    context.linkstore.save_link(context.an_url, given_tag)

@when(u'I retrieve all links with tag "{given_tag}"')
def retrieve_all_links_with_given_tag(context, given_tag):
    context.all_links_with_given_tag = context.linkstore.find_by_tag(given_tag)

@then(u'I should get that link\'s URL and the date when that link was saved')
def verify_saved_link_is_present(context):
    expect(context.all_links_with_given_tag).to(
        contain(tuple_containing(context.an_url, context.a_date))
    )
