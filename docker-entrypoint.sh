#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python /app/manage.py migrate

# Start server
echo "Starting server"
python /app/manage.py runserver 0.0.0.0:8000