from click import group, argument

from . import factory


linkstore = factory.create()

@group()
def linkstore_cli():
    pass

@linkstore_cli.command()
@argument('url')
@argument('tags', nargs=-1, required=True)
def save(url, tags):
    linkstore.save_link(url, tags)


@linkstore_cli.command()
@argument('tag_filter', required=False)
def list(tag_filter):
    if tag_filter is None:
        print_all_links()
    else:
        print_without_tags_links_tagged_with(tag_filter)


def print_all_links():
    for link in linkstore.get_all():
        print('  |  '.join([link[0], link[1], '#' + ', #'.join(link[2])]))

def print_without_tags_links_tagged_with(tag_filter):
    for matching_link in linkstore.find_by_tag(tag_filter):
        print('  |  '.join([matching_link[0], matching_link[1]]))
