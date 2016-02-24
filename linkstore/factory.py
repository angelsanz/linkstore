from .link import Link
from .linkstore import Linkstore
from .link_storage import SqliteLinkStorage, SqliteConnectionFactory


def create_linkstore():
    return Linkstore(
        SqliteLinkStorage(
            SqliteConnectionFactory.create_autoclosing_on_disk()
        ),
        create_link
    )

def create_link(link_record):
    return Link(*link_record)
