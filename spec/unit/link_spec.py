from expects import expect, equal

from linkstore.link import Link


with description('Link'):
    with context('is a value object'):
        with it('respects equality'):
            expect(
                Link('an url', ('a tag',), 'a date')
            ).to(equal(
                Link('an url', ('a tag',), 'a date')
            ))

        with it('respects non-equality'):
            pairs_of_different_links = [
                (Link('an url', ('a tag',), 'a date'), Link('another url', ('a tag',),       'a date')),
                (Link('an url', ('a tag',), 'a date'), Link('an url',      ('another tag',), 'a date')),
                (Link('an url', ('a tag',), 'a date'), Link('an url',      ('a tag',),       'another date')),
                (Link('an url', ('a tag',), 'a date'), Link('another url', ('another tag',), 'a date')),
                (Link('an url', ('a tag',), 'a date'), Link('another url', ('a tag',),       'another date')),
                (Link('an url', ('a tag',), 'a date'), Link('an url',      ('another tag',), 'another date')),
                (Link('an url', ('a tag',), 'a date'), Link('another url', ('another tag',), 'another date'))
            ]

            for a_link, a_different_link in pairs_of_different_links:
                expect(a_link).not_to(equal(a_different_link))
