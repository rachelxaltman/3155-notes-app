Feature: Signing out of a user’s account
Background:
    Given A user is signed in and is on the webpage

Scenario: A user is trying to log out of their account
    Given that user is on the website and logged in
    When the user clicks the logout button
    Then the webapp should log the user out
    And the webpage will be redirected to the login/signup page