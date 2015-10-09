Feature: Apache

  Scenario: Default content is served
    When couchdb container is started
    Then port 5984 is open