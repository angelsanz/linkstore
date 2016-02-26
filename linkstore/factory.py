from .link import Link
from .linkstore import Linkstore
from .link_storage import SqliteLinkStorage, SqliteConnectionFactory, LinksTable, TagsTable


def create_linkstore():
    return Linkstore(
        create_sqlite_link_storage_with_connection(
            SqliteConnectionFactory.create_autoclosing_on_disk()
        ),
        create_link
    )

def create_sqlite_link_storage_with_connection(connection):
    return SqliteLinkStorage({
        'links': LinksTable(connection),
        'tags': TagsTable(connection)
    })

def create_link(link_record):
    return Link(*link_record)
