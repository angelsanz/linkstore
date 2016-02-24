import random

from doublex import Stub

from linkstore.link import Link
from linkstore.factory import create_link


def some_links():
    return map(create_link, data_for_some_links())

def data_for_some_links():
    return [
        ('https://www.example.com/',        ('favourites',),                      '12/03/2008'   ),
        ('https://www.another-example.net', ('misc',),                            '35/56/89'     ),
        ('https://one-more.org',            ('bla', 'ble'),                       '789/23/677785'),
        ('an url',                          ('a tag',),                           '18/12/2015'   ),
        ('another url',                     ('another tag',),                     'a date'       ),
        ('one more url',                    ('a different tag',),                 'another date' ),
        ('and one more',                    ('with one tag', 'and one more tag'), 'whatever date')
    ]

def one_link():
    return random.choice(some_links())

def some_stubbed_links():
    return map(create_stubbed_link, data_for_some_links())

def create_stubbed_link(link_record):
    return LinkStub(*link_record)

def LinkStub(url, tags, date):
    with Stub(Link) as link_stub:
        link_stub.url.returns(url)
        link_stub.tags.returns(tags)
        link_stub.date.returns(date)

    return link_stub

def some_stubbed_links_with_tags(tags):
    return [
        LinkStub(url, tags, date)
        for url, _, date in data_for_some_links()
    ]
