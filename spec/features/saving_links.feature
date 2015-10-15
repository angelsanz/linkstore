Feature: Saving links
    Allow the saving of URLs with one or more tags.

    Scenario: saving a link with one tag
        Given an URL and a tag
        When I request that they be saved
        Then they should be successfully saved
