#! /bin/bash

rm -f /home/michael/simmgr.sqlite

echo "no" | python manage.py syncdb

