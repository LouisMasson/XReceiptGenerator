# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
