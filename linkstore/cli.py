import click
from click import group, argument

from linkstore import factory
from linkstore.clock import Clock


links_service = factory.create_links_service_with(factory.create_persistent_links())
handles = factory.create_handles()
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
    for link in links_service.get_all():
        print('  |  '.join([
            str(handles.compute_for(link.url)),
            link.url,
            link.date,
            '#' + ', #'.join(link.tags)
        ]))

def print_without_tags_links_tagged_with(tag_filter):
    for link in links_service.retrieve_links_by_tag(tag_filter):
        print('  |  '.join([
            str(handles.compute_for(link.url)),
            link.url,
            link.date
        ]))


@cli.command()
@argument('handle', type=click.INT)
@argument('current_tag')
@argument('new_tag')
def retag(handle, current_tag, new_tag):
    url = handles.retrieve_url_from(handle)
    links_service.modify_tag_of_link_with_url(url, {current_tag: new_tag})


@cli.command()
@argument('handle', type=click.INT)
@argument('new_tags', nargs=-1, required=True)
def tag(handle, new_tags):
    url = handles.retrieve_url_from(handle)
    links_service.add_tags_to_link_with_url(url, new_tags)


@cli.command()
@argument('handle', type=click.INT)
def delete(handle):
    url = handles.retrieve_url_from(handle)
    links_service.delete_link_with_url(url)


@cli.command('rename-tag')
@argument('current_tag')
@argument('new_tag')
def rename_tag(current_tag, new_tag):
    links_service.modify_tag_of_all_links({current_tag: new_tag})
