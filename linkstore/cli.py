from click import group, argument

from . import factory
from .link import Link
from .clock import Clock


linkstore = factory.create_linkstore()
clock = Clock()


@group()
def linkstore_cli():
    pass

@linkstore_cli.command()
@argument('url')
@argument('tags', nargs=-1, required=True)
def save(url, tags):
    linkstore.save(Link(url, tags, clock.date_of_today()))


@linkstore_cli.command()
@argument('tag_filter', required=False)
def list(tag_filter):
    if tag_filter is None:
        print_all_links()
    else:
        print_without_tags_links_tagged_with(tag_filter)


def print_all_links():
    for link in linkstore.get_all():
        print('  |  '.join([link.url, link.date, '#' + ', #'.join(link.tags)]))

def print_without_tags_links_tagged_with(tag_filter):
    for matching_link in linkstore.find_by_tag(tag_filter):
        print('  |  '.join([matching_link.url, matching_link.date]))
