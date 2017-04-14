from .link import Link


class LinksService(object):
    def __init__(self, link_storage, link_creator):
        self._storage = link_storage
        self._link_creator = link_creator

    def save_link(self, url, tags, date):
        link = Link(url, tags, date)
        self._storage.save(link)

    def retrieve_links_by_tag(self, tag):
        return self._create_links_from_link_records(self._storage.find_by_tag(tag))

    def _create_links_from_link_records(self, link_records):
        return [
            self._link_creator(record)
            for record in link_records
        ]

    def get_all(self):
        return self._create_links_from_link_records(self._storage.get_all())

    def delete_link_with_url(self, url):
        self._storage.delete_link_with_url(url)

    def modify_tag_of_link_with_url(self, url, tag_modification):
        self._storage.replace_tag_in_link_with_url(url, tag_modification)

    def modify_tag_of_all_links(self, tag_modification):
        self._storage.replace_tag_globally(tag_modification)

    def add_tags_to_link_with_url(self, url, tags):
        self._storage.add_tags_to_link_with_url(url, tags)
