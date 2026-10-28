# ============================================================
# Experiment 5: Docker Containerization
# ============================================================
# AIM: To learn Docker containerization of a Python Flask
#      web application.
#
# This Dockerfile creates a container for the Online Book Store
# Flask API.
# ============================================================

# Stage 1: Base image - Use slim Python for smaller image
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Jay Student <jay@obs.com>"
LABEL version="1.0"
LABEL description="Online Book Store - Flask API"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user for security (best practice)
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose the application port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Start command
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
