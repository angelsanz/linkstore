from .links_service import LinksService
from .links import Links, SqliteLinks, SqliteConnectionFactory, LinksTable, TagsTable
from .handles import Handles, HandlesTable


def create_links_service():
    return LinksService(Links())

def create_links_service_with(links):
    return LinksService(links)

def create_persistent_links():
    connection = SqliteConnectionFactory.create_autoclosing_on_disk()
    return SqliteLinks({
        'links': LinksTable(connection),
        'tags': TagsTable(connection)
    })

def create_handles():
    connection = SqliteConnectionFactory.create_autoclosing_on_disk()
    return Handles(HandlesTable(connection))
