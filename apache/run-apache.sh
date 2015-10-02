#!/bin/bash

# Make sure we're not confused by old, incompletely-shutdown httpd
# context after restarting the container.  httpd won't start correctly
# if it thinks it is already running.
rm -rf /run/httpd/* /tmp/httpd*
# /etc/httpd/logs is a file?
rm -rf /etc/httpd/logs
mkdir -p /etc/httpd/logs

exec /usr/sbin/httpd -D FOREGROUND
