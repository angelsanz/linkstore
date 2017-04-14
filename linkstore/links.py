class Links(object):
    def __init__(self):
        self._links = {}

    def add(self, link):
        self._links[link.url] = link

    def find_by_tag(self, tag):
        return [link for link in self._links.values() if tag in link.tags]
