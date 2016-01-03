from expects import expect, contain, equal
from doublex import Stub

from linkstore.linkstore import Linkstore
from linkstore.link_storage import SqliteLinkStorage, SqliteConnectionFactory
from linkstore.clock import Clock


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




@given(u'I have saved the URL "{an_url}" with tag "{given_tag}" on "{given_date}"')
def save_link_with_given_tag(context, an_url, given_tag, given_date):
    context.an_url = an_url
    context.a_date = given_date
    context.linkstore = Linkstore(an_in_memory_sqlite_link_storage_on_date(context.a_date))

    context.linkstore.save_link(context.an_url, given_tag)

@when(u'I retrieve all links with tag "{given_tag}"')
def retrieve_all_links_with_given_tag(context, given_tag):
    context.all_links_with_given_tag = context.linkstore.find_by_tag(given_tag)

@then(u'I should get that link\'s URL and the date when that link was saved')
def verify_saved_link_is_present(context):
    expect(context.all_links_with_given_tag).to(
        contain(tuple_containing(context.an_url, context.a_date))
    )



@given(u'I have saved the links')
def save_links_from_context_table(context):
    context.saved_links = []
    connection = SqliteConnectionFactory.create_in_memory()

    for link_row in context.table:
        context.linkstore = Linkstore(SqliteLinkStorage(connection, stubbed_clock_on_date(link_row['date saved'])))

        link_to_save = (link_row['URL'], (link_row['tag'],))
        context.linkstore.save_link(*link_to_save)
        context.saved_links.append(link_to_save)

@when(u'I retrieve all links')
def retrieve_all_links(context):
    context.all_links = context.linkstore.get_all()

@then(u'I should get all the previously saved links')
def verify_all_saved_links_are_present(context):
    expect(len(context.all_links)).to(equal(len(context.saved_links)))

    for saved_link in context.saved_links:
        expect(context.all_links).to(
            contain(tuple_containing(*saved_link))
        )


def tuple_containing(*values):
    return contain(*values)

def an_in_memory_sqlite_link_storage_on_any_date():
    return an_in_memory_sqlite_link_storage_on_date('18/12/2015')

def an_in_memory_sqlite_link_storage_on_date(a_date):
    return SqliteLinkStorage(
        SqliteConnectionFactory.create_in_memory(),
        stubbed_clock_on_date(a_date)
    )

def stubbed_clock_on_date(a_date):
    with Stub(Clock) as clock_stub:
        clock_stub.date_of_today().returns(a_date)

    return clock_stub
