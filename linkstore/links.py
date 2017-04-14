class Links(object):
    def __init__(self):
        self._links = {}

    def add(self, link):
        self._links[link.url] = link

    def find_by_tag(self, tag):
        return [link for link in self._links.values() if tag in link.tags]

    def get_all(self):
        return self._links.values()

    def remove(self, link):
        del self._links[link.url]

    def find_by_url(self, url):
        return self._links[url]
