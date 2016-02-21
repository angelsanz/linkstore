Feature: Saving links
    Allow the saving
    of URLs
    with one or more tags.

    Scenario: saving a link with one tag
        Given an URL and a tag
        When I request that the URL be saved with that tag
        Then they should be successfully saved

    Scenario: saving a link with more than one tag
        Given an URL and some tags
        When I request that the URL be saved with those tags
        Then they should be successfully saved
