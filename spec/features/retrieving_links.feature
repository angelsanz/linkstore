Feature: Retrieving links
    Allow the retrieval
    of one or more
    of the previously-saved links 

    Scenario: Retrieving links by one tag
        Scenario: Only some links have been saved with exactly that tag
            Given I have saved some URLs with the target tag on a certain date
            When I retrieve all links with that tag
            Then I should get the links I originally saved with the target tag

        Scenario: Only some links have been saved with that tag and some more tags
            Given I have saved some URLs with the target tag and some more tags on a certain date
            When I retrieve all links with the target tag
            Then I should get the links I originally saved with the target tag and some more tags

        Scenario: Some links have been saved with exactly that tag but
        other links have been saved with different tags
            Given I have saved some URLs with the target tag on a certain date
            And I have saved some more URLs each with a tag different from the target tag
            When I retrieve all links with the target tag
            Then I should get the links I originally saved with the target tag

    Scenario: Retrieving all links
        Given I have saved some links
        When I retrieve all links
        Then I should get all the links I had saved
