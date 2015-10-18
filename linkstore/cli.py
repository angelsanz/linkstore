from click import group, argument

from .linkstore import Linkstore


linkstore = Linkstore()

@group()
def linkstore_cli():
    pass

@linkstore_cli.command()
@argument('url')
@argument('tag')
def save(url, tag):
    linkstore.save_link(url, tag)


@linkstore_cli.command()
@argument('tag_filter')
def list(tag_filter):
    matching_links = linkstore.find_by_tag(tag_filter)

    for matching_link in matching_links:
        print(matching_link[0])
