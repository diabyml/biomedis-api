#!/bin/bash
# start.sh - Start script for Render.com

echo "🚀 Starting Biomedis api..."

# Check if we need to run migrations
echo "🗄️ Checking for database migrations..."
alembic upgrade head

# Start the application
echo "🌐 Starting server..."
exec gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000