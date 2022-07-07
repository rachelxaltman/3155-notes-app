Feature: Add a new note 
Background:
    Given:a user is signed in  and wants to add or create a desired note 


Scenario: A user wants to add notes 
    Given that the user is already signed in and wants to create a new note
    When when the user clicks on Add a new note 
    Then a box that allow user to create a note will pop up 
    And the user will be able to create a new note
