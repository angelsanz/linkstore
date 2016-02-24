class Link(object):
    def __init__(self, url, tags, date):
        self._url = url
        self._tags = tags
        self._date = date

    @property
    def url(self):
        return self._url

    @property
    def tags(self):
        return self._tags

    @property
    def date(self):
        return self._date

    def __eq__(self, other):
        return all([
            self.url == other.url,
            self.tags == other.tags,
            self.date == other.date
        ])

    def __ne__(self, other):
        return not self.__eq__(other)

    __hash__ = None
