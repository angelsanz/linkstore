class LinkStorage(object):
    def __init__(self):
        self._links = []

    def get_all(self):
        return self._links

    def save(self, an_url, a_tag):
        self._links.append((an_url, a_tag))
