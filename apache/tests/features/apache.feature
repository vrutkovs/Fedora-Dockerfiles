Feature: Apache

  Scenario: Default content is served
    When apache container is started
    Then default apache content is served on 80 port