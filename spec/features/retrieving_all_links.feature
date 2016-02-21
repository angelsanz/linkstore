Feature: Retrieving all links
    Allow the retrieval
    of all the links
    which have been saved.


    Scenario: Retrieving all links
        Given I have saved some links
        When I retrieve all links
        Then I should get all the links I had saved
