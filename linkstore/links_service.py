from .link import Link


class LinksService(object):
    def __init__(self, link_storage, links, link_creator):
        self._storage = link_storage
        self._link_creator = link_creator
        self._links = links

    def save_link(self, url, tags, date):
        link = Link(url, tags, date)
        self._storage.save(link)
        self._links.add(link)

    def retrieve_links_by_tag(self, tag):
        self._create_links_from_link_records(self._storage.find_by_tag(tag))

        return self._links.find_by_tag(tag)


    def _create_links_from_link_records(self, link_records):
        return [
            self._link_creator(record)
            for record in link_records
        ]

    def get_all(self):
        self._create_links_from_link_records(self._storage.get_all())

        return self._links.get_all()

    def delete_link_with_url(self, url):
        self._storage.delete_link_with_url(url)

        link = self._links.find_by_url(url)
        self._links.remove(link)

    def modify_tag_of_link_with_url(self, url, tag_modification):
        self._storage.replace_tag_in_link_with_url(url, tag_modification)

        link = self._links.find_by_url(url)
        self._links.add(link.modify_tag(tag_modification))

    def modify_tag_of_all_links(self, tag_modification):
        self._storage.replace_tag_globally(tag_modification)

        for link in self._links.get_all():
            self._links.add(link.modify_tag(tag_modification))

    def add_tags_to_link_with_url(self, url, tags):
        self._storage.add_tags_to_link_with_url(url, tags)

        link = self._links.find_by_url(url)
        self._links.add(link.add_tags(tags))
