#!/usr/bin/env bash
set -o errexit

# Run database migrations against the persistent disk database path (/data/db.sqlite3)
python manage.py migrate

# Start the Gunicorn web server
gunicorn constructionmanagement.wsgi:application --bind 0.0.0.0:$PORT