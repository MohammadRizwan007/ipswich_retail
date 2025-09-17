# FROM python:3.11-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# # System dependencies (SQLite is built-in, no extra needed)
# RUN apt-get update && apt-get install -y build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Copy project files
# COPY . /app

# # Collect static files
# # RUN python manage.py collectstatic --noinput

# # Add non-root user
# RUN useradd -m appuser
# USER appuser

# # Create entrypoint script
# RUN echo '#!/bin/bash\n\
# python manage.py migrate --noinput\n\
# python manage.py collectstatic --noinput\n\
# exec gunicorn Ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 3' > /app/entrypoint.sh

# RUN chmod +x /app/entrypoint.sh

# # Use the entrypoint script
# CMD ["/app/entrypoint.sh"]


# # Start Django with gunicorn
# # CMD gunicorn Ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 3
# # CMD sh -c "python manage.py collectstatic --noinput && gunicorn Ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 3"


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

# Create all necessary directories with proper permissions
RUN mkdir -p /app/media /app/media/products /app/staticfiles && \
    chmod -R 775 /app/media && \
    chmod -R 755 /app/staticfiles

# Add non-root user and set ownership
RUN useradd -m appuser && \
    chown -R appuser:appuser /app && \
    chown -R appuser:appuser /app/media && \
    chown -R appuser:appuser /app/media/products

USER appuser

# Run migrations, collect static files, and start gunicorn
CMD bash -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn Ecommerce.wsgi:application --bind 0.0.0.0:\${PORT:-8000} --workers 3"



# FROM python:3.11-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# # System dependencies
# RUN apt-get update && apt-get install -y build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Copy project files
# COPY . /app

# # Create staticfiles directory (permissions safe)
# RUN mkdir -p /app/staticfiles

# # Add non-root user and set ownership
# RUN useradd -m appuser && \
#     chown -R appuser:appuser /app
# USER appuser

# # before USER appuser
# RUN chown -R appuser:appuser /app/media

# # Run migrations, collect static files, and start gunicorn
# CMD bash -c "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn Ecommerce.wsgi:application --bind 0.0.0.0:\${PORT:-8000} --workers 3"
