Feature: MariaDB connection

  Background:
    Given mariadb container param "USER" is set to "user"
      And mariadb container param "PASS" is set to "pass"
      And mariadb container param "NAME" is set to "db"

  Scenario: User account - smoke test
    When mariadb container is started
    Then mariadb connection can be established

  Scenario: Root account - smoke test
    Given mariadb container param "ROOT_PASS" is set to "root_passw"
     When mariadb container is started
     Then mariadb connection with parameters can be established:
          | param | value      |
          | USER  | root       |
          | PASS  | root_passw |
          | NAME  | db         |

  Scenario Outline: Incorrect connection data - user account
    When mariadb container is started
    Then mariadb connection with parameters can not be established:
          | param | value      |
          | USER  | <user>     |
          | PASS  | <password> |
          | NAME  | <db>       |

    Examples:
    | user      | password | db  |
    | userr     | pass     | db  |
    | user      | passs    | db  |
    | user      | pass     | db1 |
    | \$invalid | pass     | db  |
    | user      | '        | db  |
    | user      | pass     | $invalid  |
    | user      | pass     | very_long_database_name_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  |
    | very_long_username | pass     | db  |

  Scenario Outline: Incorrect connection data - root account
    Given mariadb container param "ROOT_PASS" is set to "root_passw"
     When mariadb container is started
    Then mariadb connection with parameters can not be established:
          | param | value      |
          | USER  | root       |
          | PASS  | <password> |
          | NAME  | <db>       |

    Examples:
    | password    | db  |
    | root_passw1 | db  |
    | root_passw  | db1 |
    | '           | db  |

  Scenario: Incomplete params
    When mariadb container is started
    Then mariadb connection with parameters can not be established:
          | param | value |
          | USER  | user  |
          | PASS  | pass  |
     And mariadb connection with parameters can not be established:
          | param | value |
          | USER  | user  |
          | NAME  | pass  |
     And mariadb connection with parameters can not be established:
          | param | value |
          | PASS  | pass  |
          | NAME  | pass  |