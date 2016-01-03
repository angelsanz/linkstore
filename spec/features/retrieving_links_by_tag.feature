Feature: Retrieving links by tag
    Allow the retrieval
    of one or more
    of the previously-saved links
    by specifying
    some of the tags
    with which they were saved.

    Scenario: Retrieving by one tag
        Given I have saved the URL "https://www.example.com/" with tag "favourites" on "8/12/2015"
        When I retrieve all links with tag "favourites"
        Then I should get that link's URL and the date when that link was saved
