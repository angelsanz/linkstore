Feature: Changing the tags of existing links
    Allow the
        modification,
        addition,
        or deletion
    of
        some
        or all
    of
        the tags
    of
        an existing link
        or links.

    Scenario: Modifying one tag for one link
        Given I have saved an URL with a tag
        When I modify the tag to a new, different tag
        Then that link should have the new tag
        And that link should not have the original tag

    Scenario: Modifying one tag for all links
        Given I have saved some URLs with a tag
        When I modify the tag to a new, different tag
        Then those links should have the new tag
        And those links should not have the original tag

    Scenario: Adding one or more tags
        Given I have saved an URL with a tag
        When I add some new tags to that link
        Then that link should have the original tags
        And the new tags

    Scenario: Deleting one tag from links with more than one tag

    Scenario: Deleting one tag from links with one tag

    Scenario: Deleting n tags from links with more than n tags

    Scenario: Deleting n tags from links with n tags or less

    Scenario: Deleting tags which don't exist
