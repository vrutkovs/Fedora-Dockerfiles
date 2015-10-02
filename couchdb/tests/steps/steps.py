# -*- coding: utf-8 -*-
from common_steps.common_connection_steps import *
from common_steps.common_docker_steps import *


@when(u'couchdb container is started')
def couchdb_container_is_started(context):
    # Read mariadb params from context var
    params = '--name=ctf --privileged=true'
    context.execute_steps(u'* Docker container is started with params "%s"' % params)
    sleep(10)


@then(u'default apache content is served on {port:d} port')
def apache_content(context, port):
    for attempts in xrange(0, 5):
        context.ip = context.run("docker inspect --format='{{.NetworkSettings.IPAddress}}' %s" % context.cid).strip()
        if context.ip:
            break
        sleep(1)

    if not context.ip:
        raise Exception("No IP got assigned to container")

    context.execute_steps(u'* port %s is open' % port)

    output = None
    for attempts in xrange(0, 5):
        try:
            output = context.run('curl http://%s:%s' % (context.ip, port))
            break
        except AssertionError:
            sleep(5)

    if not output:
        raise Exception("Failed to connect to apache")
    else:
        assert output == 'Apache', 'Expected "Apache", but got "%s"' % output
