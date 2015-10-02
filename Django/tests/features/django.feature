Feature: Django connection

  Scenario: Root account - positive test
    When django container is started
    Then port 8080 is open