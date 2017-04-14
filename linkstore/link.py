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

    def modify_tag(self, tag_modification):
        current_tag = tag_modification.keys()[0]
        new_tag = tag_modification[current_tag]

        def update(tag):
            if tag != current_tag:
                return tag
            return new_tag

        new_tags = tuple({ update(tag) for tag in self.tags })

        return Link(self.url, new_tags, self.date)

    def add_tags(self, tags):
        return Link(self.url, self.tags + tags, self.date)


    def __eq__(self, other):
        return all([
            self.url == other.url,
            self.tags == other.tags,
            self.date == other.date
        ])

    def __ne__(self, other):
        return not self.__eq__(other)

    __hash__ = None


class LinkRecord(object):
    def __init__(self, link_id, *parameters_for_link_constructor):
        self._id = str(link_id)
        self._link = Link(*parameters_for_link_constructor)

    @property
    def id(self):
        return self._id

    @property
    def url(self):
        return self._link.url

    @property
    def tags(self):
        return self._link.tags

    @property
    def date(self):
        return self._link.date

    def toLink(self):
        return self._link
