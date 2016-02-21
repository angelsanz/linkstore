Feature: Retrieving links by tag
    Allow the retrieval
    of one or more
    of the previously-saved links
    by specifying
    some of the tags
    with which they were saved.

    Scenario: Retrieving by one tag
        Given I have saved an URL with a tag on a certain date
        When I retrieve all links with that tag
        Then I should get that link's URL and the date when it was saved
