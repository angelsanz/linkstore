from .link import Link


class LinksService(object):
    def __init__(self, links):
        self._links = links

    def save_link(self, url, tags, date):
        link = Link(url, tags, date)
        self._links.add(link)

    def retrieve_links_by_tag(self, tag):
        return self._links.find_by_tag(tag)

    def get_all(self):
        return self._links.get_all()

    def delete_link_with_url(self, url):
        link = self._links.find_by_url(url)
        self._links.remove(link)

    def modify_tag_of_link_with_url(self, url, tag_modification):
        link = self._links.find_by_url(url)
        self._links.add(link.modify_tag(tag_modification))

    def modify_tag_of_all_links(self, tag_modification):
        for link in self._links.get_all():
            self._links.add(link.modify_tag(tag_modification))

    def add_tags_to_link_with_url(self, url, tags):
        link = self._links.find_by_url(url)
        self._links.add(link.add_tags(tags))
