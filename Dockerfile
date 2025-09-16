FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies (SQLite is built-in, no extra needed)
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Add non-root user
RUN useradd -m appuser
USER appuser

# Start Django with gunicorn
CMD gunicorn Ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 3

