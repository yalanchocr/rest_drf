#!/bin/bash
supervisord -c /etc/supervisor/supervisord.conf
tail -f /dev/null /var/log/nginx/*.log /var/log/gunicorn/*.log