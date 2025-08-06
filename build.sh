#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating staticfiles directory..."
mkdir -p staticfiles

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Setting up production environment..."
python manage.py setup_production

echo "Build completed successfully!"
