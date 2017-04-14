from .links_service import LinksService
from .link_storage import SqliteLinkStorage, SqliteConnectionFactory, LinksTable, TagsTable


def create_links_service_with_storage(storage):
    return LinksService(
        storage,
        create_link
    )

def create_sqlite_link_storage():
    return create_sqlite_link_storage_with_connection(
        SqliteConnectionFactory.create_autoclosing_on_disk()
    )

def create_sqlite_link_storage_with_connection(connection):
    return SqliteLinkStorage({
        'links': LinksTable(connection),
        'tags': TagsTable(connection)
    })

def create_link(link_record):
    return link_record.toLink()
