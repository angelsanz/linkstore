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
            self._link_creator(record)
            for record in link_records
        ]

    def get_all(self):
        return self._create_links_from_link_records(self._storage.get_all())

    def delete(self, link):
        self._storage.delete_link_with_url(link.url)

    def modify_tag(self, link, tag_modification):
        self._storage.replace_tag_in_link_with_url(link.url, tag_modification)

    def add_tags(self, link, tags):
        self._storage.add_tags_to_link_with_url(link.url, tags)
