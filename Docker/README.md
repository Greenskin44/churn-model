# Iranian Churn Prediction API - Docker Deployment Guide

This directory contains the containerized deployment setup for the Iranian Churn Prediction Flask API that corresponds to the Jupyter notebook preprocessing pipeline.

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Build and run the production API:**
   ```bash
   docker-compose up --build -d
   ```

2. **Access the API:**
   - API Base URL: http://localhost:5000
   - Health Check: http://localhost:5000/health
   - Features Info: http://localhost:5000/features

3. **Test the API:**
   ```bash
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
       "Call_Failure": 0,
       "Subscription_Length": 24,
       "Charge_Amount": 50.5,
       "Seconds_of_Use": 1200,
       "Frequency_of_use": 15,
       "Frequency_of_SMS": 8,
       "Distinct_Called_Numbers": 5,
       "Age_Group": 3,
       "Age": 35,
       "Customer_Value": 150.75,
       "Complains": 0,
       "Tariff_Plan": 1,
       "Status": 1
     }'
   ```

### Using Docker Directly

1. **Build the image:**
   ```bash
   docker build -t iranian-churn-api .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 5000:5000 --name churn-api iranian-churn-api
   ```

## 🛠️ Development Setup

For development with live code reloading:

```bash
docker-compose --profile dev up --build
```

This runs a development version on port 5001 with volume mounting for live updates.

## 📁 Project Structure

```
├── Dockerfile                              # Production container definition
├── docker-compose.yml                      # Multi-service deployment
├── requirements-docker.txt                 # Streamlined production dependencies
├── .dockerignore                          # Files excluded from build context
├── Churn-prediction/
│   ├── Flask_API/
│   │   └── Churn_Model_Deployment_Lab.py  # Main Flask application
│   └── model/
│       └── Optimized_IRN_churn_prediction_model.pkl  # Trained model
```

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV`: Set to 'production' or 'development'
- `FLASK_DEBUG`: Enable debug mode (development only)
- `PYTHONUNBUFFERED`: Ensure Python output is not buffered

### Docker Configuration

- **Base Image**: `python:3.9-slim` for optimal size/compatibility balance
- **Security**: Runs as non-root user (`appuser`)
- **Health Checks**: Built-in health monitoring via `/health` endpoint
- **Port**: Exposes port 5000

## 📊 API Endpoints

- `GET /` - Welcome message and API information
- `POST /predict` - Make churn predictions (requires JSON payload)
- `GET /features` - Get expected feature schema and example
- `GET /health` - Health check and API status

## 🔍 Monitoring & Logs

### View container logs:
```bash
docker-compose logs -f churn-api
```

### Check container health:
```bash
docker-compose ps
curl http://localhost:5000/health
```

## 🛡️ Security Features

- Non-root user execution
- Minimal production dependencies
- Health check monitoring
- Input validation and error handling

## 🚀 Production Deployment

For production deployments, consider:

1. **Use Gunicorn** (uncomment in Dockerfile):
   ```dockerfile
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "Churn_Model_Deployment_Lab:app"]
   ```

2. **Add reverse proxy** (nginx) for SSL termination
3. **Implement logging aggregation**
4. **Set up monitoring** (Prometheus/Grafana)
5. **Configure resource limits**

## 🧹 Cleanup

Stop and remove containers:
```bash
docker-compose down
```

Remove images:
```bash
docker rmi iranian-churn-api
```

## 📝 Notes

- The model file must be present in `Churn-prediction/model/` directory
- The API preprocessing pipeline exactly matches the Jupyter notebook workflow
- Container includes health checks for production reliability
- Optimized for both development and production use cases
