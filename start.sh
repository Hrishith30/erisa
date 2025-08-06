#!/usr/bin/env bash

# Get the port from Render's environment variable
PORT="${PORT:-8000}"

# Start gunicorn with the correct bind address
exec gunicorn claims_interface.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
