FROM ubuntu:latest
LABEL authors="Owner"

ENTRYPOINT ["top", "-b"]

# Use a compatible Python version
FROM python:3.9-slim

# Set up the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Update pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app

# Expose the necessary port
EXPOSE 5000

# Run the application
CMD ["python", "Churn_Model_Deployment_Lab.py"]


