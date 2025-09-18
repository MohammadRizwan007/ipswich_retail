FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app

# Create staticfiles directory (not media; volume handles media permissions)
RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

# Add non-root user and set ownership for app files
# RUN useradd -m appuser && chown -R appuser:appuser /app
# USER appuser
USER root

# Run migrations, collect static files, and start gunicorn
CMD bash -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn Ecommerce.wsgi:application --bind 0.0.0.0:\${PORT:-8000} --workers 3"

