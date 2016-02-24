class Linkstore(object):
    def __init__(self, link_storage, link_creator):
        self._storage = link_storage
        self._link_creator = link_creator

    def save(self, link):
        self._storage.save(link)

    def find_by_tag(self, tag):
        return self._create_links_from_link_records(self._storage.find_by_tag(tag))

    def _create_links_from_link_records(self, link_records):
        return [
            self._link_creator(link_record)
            for link_record in link_records
        ]

    def get_all(self):
        return self._create_links_from_link_records(self._storage.get_all())
