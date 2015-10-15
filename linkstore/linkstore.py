from .link_storage import LinkStorage

class Linkstore(object):
    def __init__(self, link_storage=None):
        self._storage = link_storage if link_storage is not None else LinkStorage()

    def save_link(self, an_url, a_tag):
        self._storage.save(an_url, a_tag)
