Feature: Editing a user’s note
Background: 
    Given A user has notes

Scenario: A user is trying to edit their note
    Given that the user is logged in and has selected a note
    When the user clicks edit on a note
    Then the webapp should open the note to be edited
    And the webpage will allow the user to post an edit to the note