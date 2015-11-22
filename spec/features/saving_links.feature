Feature: Saving links
    Allow the saving of URLs with one or more tags.

    Scenario: saving a link with one tag
        Given an URL and a tag
        When I request that they be saved
        Then they should be successfully saved

    Scenario: saving a link with more than one tag
        Given the URL "https://www.example.com/" and the tags "favourites", "misc"
        When I request that the link be saved with those tags
        Then they it should be successfully saved
