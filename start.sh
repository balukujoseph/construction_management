#!/usr/bin/env bash
set -o errexit

# Make sure the persistent disk directory exists
mkdir -p /data

# Run database migrations against the persistent disk database
python manage.py migrate

# Start the Gunicorn web server
gunicorn constructionmanagement.wsgi:application --bind 0.0.0.0:$PORT