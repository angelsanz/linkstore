from linkstore.link_storage import SqliteLinkStorage, LinksTable, TagsTable


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


class SqliteLinks(object):
    def __init__(self, connection):
        self._storage = SqliteLinkStorage({
            'links': LinksTable(connection),
            'tags': TagsTable(connection)
        })

    def add(self, link):
        self._storage.save(link)

    def find_by_tag(self, tag):
        return self._storage.find_by_tag(tag)

    def get_all(self):
        return self._storage.get_all()

    def remove(self, link):
        self._storage.delete_link_with_url(link.url)

    def find_by_url(self, url):
        return self._storage.find_by_url(url)
