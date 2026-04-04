# Use python slim image for reduced size and improved security
FROM python:3.12-slim

# Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Create a non-root user to run the app for increased security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install necessary system packages for psycopg2
# We remove the lists after installation to keep the image small
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
# Copying requirements first allows leveraging Docker cache for dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    # Remove gcc after building psycopg2 to keep the image slim
    && apt-get purge -y --auto-remove gcc

# Copy application project files
COPY ./app /app/app

# Option: provide default env directly but best practice is providing via Dokploy
# COPY .env /app/.env

# Change directory ownership to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Expose port (Dokploy maps this port or uses it for routing)
EXPOSE 8000

# Start the uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
