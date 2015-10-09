Feature: Ansible connection

  Scenario: Ansible facts
    When ansible container is started
    Then container logs contain:
    """
    localhost | success >> {
    """
     And container logs contain:
     """
     "ansible_distribution": "Fedora",
     """