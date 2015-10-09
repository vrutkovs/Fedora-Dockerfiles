# -*- coding: UTF-8 -*-
from behave import when, then, given
from time import sleep
from common_steps import common_docker_steps, common_connection_steps
from random import randint



@when(u'mysql container is started')
def mysql_container_is_started(context):
    # Read mysql params from context var
    params = ' --name=ctf'
    for param in context.mysql:
        params += ' -e %s=%s' % (param, context.mysql[param])
    context.execute_steps(u'* Docker container is started with params "%s"' % params)
    sleep(10)


@given(u'mysql container param "{param}" is set to "{value}"')
def set_mysql_params(context, param, value):
    if not hasattr(context, "mysql"):
        context.mysql = {}
    context.mysql[param] = value


@then(u'mysql connection can be established')
@then(u'mysql connection can {negative:w} be established')
@then(u'mysql connection with parameters can be established')
@then(u'mysql connection with parameters can {negative:w} be established')
def mysql_connect(context, negative=False):
    if context.table:
        for row in context.table:
            context.mysql[row['param']] = row['value']

    user = context.mysql['MYSQL_USER']
    password = context.mysql['MYSQL_PASSWORD']
    db = context.mysql['MYSQL_DATABASE']

    try:
        context.execute_steps(u'* port 3306 is open')
    except Exception as e:
        if negative:
            # We're expecting the port to be closed
            return
        else:
            raise e

    for attempts in xrange(0, 5):
        try:
            context.run('docker run --rm -i --volumes-from=%s %s mysql -u"%s" -p"%s" -e "SELECT 1;" %s' % (
                context.container_id, context.image, user, password, db))
            return
        except AssertionError:
            # If  negative part was set, then we expect a bad code
            # This enables steps like "can not be established"
            if negative:
                return
            sleep(5)

    raise Exception("Failed to connect to mysql")
