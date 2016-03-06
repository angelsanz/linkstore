Feature: Deleting links
    Allow the complete deletion
    of the previously saved links.

    Scenario: deleting a link
        Given I have saved a link
        When I request that such link be deleted
        Then that link should be deleted
