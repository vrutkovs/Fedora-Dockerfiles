# -*- coding: UTF-8 -*-
from behave import when, then, given
from time import sleep
from common_steps import common_docker_steps, common_connection_steps


@when(u'ansible container is started')
def mysql_container_is_started(context):
    # Read mysql params from context var
    context.execute_steps(u'* Docker container is started with params " --privileged=true --name=ctf"')
    sleep(10)


@then(u'container logs contain')
def container_logs_contain(context):
    logs = context.run("docker logs %s" % context.get_current_cid())
    assert context.text in logs
