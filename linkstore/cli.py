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
