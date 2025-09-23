#!/bin/bash
# build.sh - Build script for Render.com

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
alembic upgrade head

echo "✅ Build completed successfully!"