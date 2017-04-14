import click
from click import group, argument

from . import factory
from .clock import Clock


link_storage = factory.create_sqlite_link_storage()
links_service = factory.create_links_service_with_storage(link_storage)
clock = Clock()


@group()
def cli():
    pass

@cli.command()
@argument('url')
@argument('tags', nargs=-1, required=True)
def save(url, tags):
    links_service.save_link(url, tags, clock.date_of_today())


@cli.command()
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


@cli.command()
@argument('link_id', type=click.INT)
@argument('current_tag')
@argument('new_tag')
def retag(link_id, current_tag, new_tag):
    link_storage.replace_tag_in_link_with_id(link_id, {current_tag: new_tag})


@cli.command()
@argument('link_id', type=click.INT)
@argument('new_tags', nargs=-1, required=True)
def tag(link_id, new_tags):
    link_storage.add_tags_to_link_with_id(link_id, new_tags)


@cli.command()
@argument('link_id', type=click.INT)
def delete(link_id):
    link_storage.delete_link_with_id(link_id)


@cli.command('rename-tag')
@argument('current_tag')
@argument('new_tag')
def rename_tag(current_tag, new_tag):
    links_service.modify_tag_globally({current_tag: new_tag})
