#!/usr/bin/env bash
set -o errexit

python manage.py migrate
gunicorn constructionmanagement.wsgi:application --bind 0.0.0.0:$PORT