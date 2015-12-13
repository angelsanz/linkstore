Feature: Saving links
    Allow the saving
    of URLs
    with one or more tags.

    Scenario: saving a link with one tag
        Given the URL "https://www.example.com/" and the tag "favourites"
        When I request that they be saved
        Then they should be successfully saved

    Scenario: saving a link with more than one tag
        Given the URL "https://www.example.com/" and the tags "favourites", "misc"
        When I request that the URL be saved with those tags
        Then the URL should be saved with those tags
