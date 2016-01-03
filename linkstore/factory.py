from .linkstore import Linkstore
from .link_storage import SqliteLinkStorage, SqliteConnectionFactory
from .clock import Clock


def create():
    return Linkstore(SqliteLinkStorage(
        SqliteConnectionFactory.create_autoclosing_on_disk(),
        Clock()
    ))
