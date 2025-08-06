#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate
