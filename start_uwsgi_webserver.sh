#!/bin/bash
cd /var/www/myapp
uwsgi --socket 0.0.0.0:5000 --protocol=http --plugin python38 --module wsgi:app --virtualenv /var/www/myapp/myenv --logto /var/log/uwsgi/myapp.log --env="FLASK_ENV=development
