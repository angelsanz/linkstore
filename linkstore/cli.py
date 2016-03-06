import click
from click import group, argument

from . import factory
from .link import Link
from .clock import Clock


link_storage = factory.create_sqlite_link_storage()
linkstore = factory.create_linkstore_with_storage(link_storage)
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
    for link_record in link_storage.get_all():
        print('  |  '.join([
            link_record.id,
            link_record.url,
            link_record.date,
            '#' + ', #'.join(link_record.tags)
        ]))

def print_without_tags_links_tagged_with(tag_filter):
    for link_record in link_storage.find_by_tag(tag_filter):
        print('  |  '.join([
            link_record.id,
            link_record.url,
            link_record.date
        ]))


@linkstore_cli.command()
@argument('link_id', type=click.INT)
@argument('current_tag')
@argument('new_tag')
def retag(link_id, current_tag, new_tag):
    link_storage.replace_tag_in_link_with_id(link_id, {current_tag: new_tag})


@linkstore_cli.command()
@argument('link_id', type=click.INT)
@argument('new_tags', nargs=-1, required=True)
def tag(link_id, new_tags):
    link_storage.add_tags_to_link_with_id(link_id, new_tags)


@linkstore_cli.command()
@argument('link_id', type=click.INT)
def delete(link_id):
    link_storage.delete_link_with_id(link_id)
