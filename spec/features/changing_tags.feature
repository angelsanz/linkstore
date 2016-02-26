Feature: Changing the tags of existing links
    Allow the modification,
    addition,
    or deletion
    of some
    or all
    of the tags
    of an existing link.

    Scenario: Modifying one tag
        Given I have saved an URL with a tag
        When I modify the tag to a new, different tag
        Then that link should have the new tag
        And that link should not have the old tag

    Scenario: Adding one tag

    Scenario: Adding more than one tag

    Scenario: Deleting one tag from links with more than one tag

    Scenario: Deleting one tag from links with one tag

    Scenario: Deleting n tags from links with more than n tags

    Scenario: Deleting n tags from links with n tags or less

    Scenario: Deleting tags which don't exist
