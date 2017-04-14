from .links_service import LinksService
from .link_storage import SqliteConnectionFactory
from .links import Links, SqliteLinks


def create_links_service():
    return LinksService(Links())

def create_links_service_with(links):
    return LinksService(links)

def create_persistent_links():
    return SqliteLinks(SqliteConnectionFactory.create_autoclosing_on_disk())
