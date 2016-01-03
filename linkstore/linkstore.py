class Linkstore(object):
    def __init__(self, link_storage):
        self._storage = link_storage

    def save_link(self, an_url, tag_or_tags):
        self._storage.save(an_url, tag_or_tags)

    def find_by_tag(self, a_tag):
        return self._storage.find_by_tag(a_tag)

    def get_all(self):
        return self._storage.get_all()
