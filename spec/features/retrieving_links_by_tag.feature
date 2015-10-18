Feature: Retrieving links
    Allow the retrieval of one or more
    of the previously-saved links.

    Scenario: Retrieving by tag
        Given I have saved a link with tag "favourites"
        When I retrieve all links with tag "favourites"
        Then I should get that link's URL
