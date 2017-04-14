from expects import expect, equal

from linkstore.link import Link
from linkstore.links import Links

from .fixtures import one_link


with description('Links repository'):
    with it('can find links by tag'):
        a_tag = 'a tag'
        link_with_tag = Link('an url', a_tag, 'a date')
        links = Links()
        links.add(link_with_tag)

        found_links = links.find_by_tag(a_tag)

        expect(found_links).to(equal([link_with_tag]))
