Feature: Retrieving links
    Allow the retrieval
    of one or more
    of the previously-saved URLs
    by specifying
    one of the tags
    with which they were saved.

    Scenario: Retrieving by one tag
        Given I have saved the URL "https://www.example.com/" with tag "favourites"
        When I retrieve all links with tag "favourites"
        Then I should get that link's URL
