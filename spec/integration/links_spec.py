from expects import expect, equal, contain

from linkstore.link import Link
from linkstore.links import Links

from ..fixtures import one_link


with description('Links repository'):
    with it('can find links by tag'):
        a_tag = 'a tag'
        link_with_tag = Link('an url', a_tag, 'a date')
        links = Links()
        links.add(link_with_tag)

        found_links = links.find_by_tag(a_tag)

        expect(found_links).to(equal([link_with_tag]))

    with it('can return all links'):
        a_link = Link(*one_link())
        links = Links()
        links.add(a_link)

        expect(links.get_all()).to(equal([a_link]))

    with it('can delete links'):
        a_link = Link(*one_link())
        links = Links()
        links.add(a_link)

        links.remove(a_link)

        expect(links.get_all()).not_to(contain(a_link))

    with it('can find links by url'):
        a_link = Link(*one_link())
        links = Links()
        links.add(a_link)

        link = links.find_by_url(a_link.url)

        expect(link).to(equal(a_link))

    with it('can add links'):
        a_link = Link(*one_link())
        links = Links()

        links.add(a_link)

        expect(links.find_by_url(a_link.url)).to(equal(a_link))
