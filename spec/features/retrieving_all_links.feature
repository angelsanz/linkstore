Feature: Retrieving all links
    Allow the retrieval
    of all the links
    which have been saved.


    Scenario: Retrieving all links
        Given I have saved the links
            | URL                               | tag          | date saved    |
            | "https://www.example.com/"        | "favourites" | 12/03/2008    |
            | "https://www.another-example.net" | "misc"       | 35/56/89      |
            | "https://one-more.org"            | "extra"      | 789/23/677785 |
        When I retrieve all links
        Then I should get all the previously saved links
