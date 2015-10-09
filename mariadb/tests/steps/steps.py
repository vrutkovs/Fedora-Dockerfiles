# -*- coding: UTF-8 -*-
from behave import when, then, given, step
import subprocess
from time import sleep
from common_steps import common_docker_steps, common_connection_steps
from random import randint


@when(u'mariadb container is started')
def mariadb_container_is_started(context):
    # Read mariadb params from context var
    context.container_id = u'ctf%s' % randint(1, 10)
    params = ' --name=%s --privileged=true' % context.container_id
    for param in context.mariadb:
        params += ' -e %s=%s' % (param, context.mariadb[param])
    context.execute_steps(u'* Docker container is started with params "%s"' % params)
    sleep(10)


@given(u'mariadb container param "{param}" is set to "{value}"')
def set_mariadb_params(context, param, value):
    if not hasattr(context, "mariadb"):
        context.mariadb = {}
    context.mariadb[param] = value


@then(u'mariadb connection can be established')
@then(u'mariadb connection can {action:w} be established')
@then(u'mariadb connection with parameters can be established')
@then(u'mariadb connection with parameters can {action:w} be established')
def mariadb_connect(context, action=False):
    if context.table:
        for row in context.table:
            context.mariadb[row['param']] = row['value']

    user = context.mariadb['MYSQL_USER']
    password = context.mariadb['MYSQL_PASSWORD']
    db = context.mariadb['MYSQL_DATABASE']

    context.execute_steps(u'* port 3306 is open')

    for attempts in xrange(0, 5):
        try:
            context.run('docker run -i --volumes-from=%s %s mysql -u"%s" -p"%s" -e "SELECT 1;" %s' % (
                context.container_id, context.image, user, password, db))
            return
        except AssertionError:
            # If  negative part was set, then we expect a bad code
            # This enables steps like "can not be established"
            if action != 'can':
                return
            sleep(5)

    raise Exception("Failed to connect to mariadb")


@step(u'local port {port:d} is open')
@step(u'local port {port:d} is {negative:w} open')
def port_open(context, port, negative=False):
    for attempts in xrange(0, 5):
        try:
            context.run('nc -w5 localhost %s < /dev/null' % port)
            return
        except subprocess.CalledProcessError:
            # If  negative part was set, then we expect a bad code
            # This enables steps like "can not be established"
            if negative:
                return
            sleep(5)
    raise Exception("Can't connect to port %s" % port)
