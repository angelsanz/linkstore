import random

from linkstore.link import Link


def some_links():
    return map(create_link_from_tuple, data_for_some_links())

def create_link_from_tuple(link_tuple):
    return Link(*link_tuple)

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

def some_links_with_tags(tags):
    return [
        create_link_from_tuple((url, tags, date))
        for url, _, date in data_for_some_links()
    ]

def a_tag_modification():
    return {
        'old tag': 'new tag'
    }
