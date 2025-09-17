#!/bin/bash
set -e

echo "Starting application..."

# Create all necessary media directories with proper permissions
echo "Setting up media directories..."
mkdir -p /app/media
mkdir -p /app/media/products
# mkdir -p /app/media/categories  # If you have category images
# mkdir -p /app/media/users       # If you have user avatars

# Set proper permissions
chmod -R 755 /app/media
chmod -R 755 /app/media/products
# chmod -R 755 /app/media/categories
# chmod -R 755 /app/media/users

# Verify permissions
echo "Checking media directory permissions..."
if [ -w "/app/media" ]; then
    echo "✓ Media directory is writable"
else
    echo "✗ Media directory is not writable - attempting to fix..."
    chmod -R 755 /app/media
fi

if [ -w "/app/media/products" ]; then
    echo "✓ Products directory is writable"
else
    echo "✗ Products directory is not writable - attempting to fix..."
    chmod -R 755 /app/media/products
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn Ecommerce.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --access-logfile -