# Iranian Churn Prediction Model - Docker Deployment
# Containerized Flask API for churn prediction with optimized Random Forest model

# Alpine image for better security and smaller footprint
FROM python:3.11-alpine

# Set metadata
LABEL authors="Owner"
LABEL description="Iranian Churn Prediction Flask API"
LABEL version="1.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=Churn_Model_Deployment_Lab.py
ENV FLASK_ENV=production

# Set working directory
WORKDIR /app

# Health check to ensure container is healthy (install curl)
RUN apk update && apk upgrade && apk add --no-cache \
    curl \
    g++ \
    gcc \
    linux-headers \
    musl-dev

# Copy requirements and install Python dependencies (use streamlined requirements)
COPY requirements-docker.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create directory structure and copy application files
COPY Churn-prediction/ ./Churn-prediction/

# Set the working directory for the Flask app
WORKDIR /app/Churn-prediction/Flask_API

# Create a non-root user for security
RUN adduser -D appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose Flask port
EXPOSE 5000

# Health check to ensure container is healthy
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the Flask application
# For development: python Churn_Model_Deployment_Lab.py
# For production: gunicorn --bind 0.0.0.0:5000 --workers 2 Churn_Model_Deployment_Lab:app
CMD ["python", "Churn_Model_Deployment_Lab.py"]


