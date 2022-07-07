Feature: Add comments
Background:
    Given: a user is signed in, and wants to add a comment

Scenario: A user wants to add comments
    Given the user is signed in and is viewing a note they have access to
    When the user clicks on the comment field
    Then they will be able to type in their comment
    And attach it to the note for them and others to see