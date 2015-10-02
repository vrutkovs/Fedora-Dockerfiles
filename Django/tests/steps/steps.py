# -*- coding: utf-8 -*-
from behave import when
from time import sleep
from common_steps import common_docker_steps, common_connection_steps


@when(u'django container is started')
def mysql_container_is_started(context):
    context.execute_steps(u'* Docker container is started with params " --privileged=true --name=ctf"')
    sleep(10)
