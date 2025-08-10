# Iranian Churn Prediction Model - Flask API Deployment
"""
This Flask API corresponds to the Iranian churn prediction notebook workflow.
It loads the optimized Random Forest model and provides prediction endpoints
with preprocessing that matches the notebook's feature engineering pipeline.
"""

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Load the trained model and preprocessing components
try:
    model = joblib.load('../model/Optimized_IRN_churn_prediction_model.pkl')
    print("✓ Model loaded successfully")
except FileNotFoundError:
    print("⚠ Model file not found. Ensure the model is saved in the correct path.")
    model = None

# Feature configuration matching the notebook preprocessing
NUMERICAL_FEATURES = [
    "call_failure",
    "subscription_length", 
    "charge_amount",
    "seconds_of_use",
    "frequency_of_use",
    "frequency_of_sms",
    "distinct_called_numbers",
    "age_group",
    "age",
    "customer_value"
]

TARIFF_PLAN = "Tariff Plan"
CATEGORICAL_FEATURES = ["Complains", TARIFF_PLAN, "Status"]

# Expected feature names after preprocessing (from notebook)
EXPECTED_FEATURES = [
    "call_failure", "subscription_length", "charge_amount", "seconds_of_use",
    "frequency_of_use", "frequency_of_sms", "distinct_called_numbers", 
    "age_group", "age", "customer_value", "complains_1", "tariff_plan_2",
    "status_1"
]

def preprocess_input(data):
    """
    Preprocess input data to match the notebook's feature engineering pipeline.
    
    Steps mirror the notebook:
    1. Handle categorical encoding (get_dummies equivalent)
    2. Standardize column names (lowercase, underscores)
    3. Scale numerical features
    4. Ensure feature order matches training
    """
    df = pd.DataFrame([data])
    
    # Convert categorical columns and create dummy variables
    for cat_feature in CATEGORICAL_FEATURES:
        if cat_feature in df.columns:
            df[cat_feature] = df[cat_feature].astype('category')
    
    # One-hot encode categorical features (drop_first=True to match notebook)
    df_encoded = pd.get_dummies(df, columns=CATEGORICAL_FEATURES, drop_first=True)
    
    # Standardize column names (matching notebook preprocessing)
    def clean_column_names(columns):
        return (columns
                .str.strip()
                .str.replace(r'\s+', ' ', regex=True)
                .str.lower()
                .str.replace(' ', '_'))
    
    df_encoded.columns = df_encoded.columns.pipe(clean_column_names)
    
    # Ensure all expected features are present
    for feature in EXPECTED_FEATURES:
        if feature not in df_encoded.columns:
            df_encoded[feature] = 0
    
    # Select and reorder features to match training
    df_final = df_encoded[EXPECTED_FEATURES]
    
    # Scale numerical features (matching notebook StandardScaler approach)
    scaler = StandardScaler()
    numerical_cols = [col for col in NUMERICAL_FEATURES if col in df_final.columns]
    df_final[numerical_cols] = scaler.fit_transform(df_final[numerical_cols])
    
    return df_final

@app.route('/', methods=['GET'])
def home():
    """API health check and information endpoint."""
    return jsonify({
        'message': 'Iranian Churn Prediction API',
        'status': 'active',
        'model_loaded': model is not None,
        'version': '1.0',
        'description': 'Predict customer churn based on Iranian telco dataset features'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict churn probability for a customer.
    
    Expected input format:
    {
        "Call Failure": 0,
        "Subscription Length": 12,
        "Charge Amount": 50.25,
        "Seconds of Use": 1500,
        "Frequency of use": 25,
        "Frequency of SMS": 10,
        "Distinct Called Numbers": 15,
        "Age Group": 2,
        "Age": 35,
        "Customer Value": 1200.50,
        TARIFF_PLAN: 1,
        "Status": 1
    }
    """
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        # Get JSON data from request
        data = request.get_json(force=True)
        
        if not data:
            return jsonify({'error': 'No input data provided'}), 400
        
        # Preprocess input data to match notebook pipeline
        processed_data = preprocess_input(data)
        
        # Make prediction
        prediction = model.predict(processed_data)[0]
        prediction_proba = model.predict_proba(processed_data)[0]
        
        # Return prediction with probabilities
        # Determine risk level based on churn probability
        if prediction_proba[1] > 0.7:
            risk_level = 'High'
        elif prediction_proba[1] > 0.3:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'

        # Construct the result dictionary
        result = {
            'churn_prediction': int(prediction),
            'churn_probability': float(prediction_proba[1]),
            'no_churn_probability': float(prediction_proba[0]),
            'risk_level': risk_level,
            'input_features_processed': len(processed_data.columns)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 400

@app.route('/features', methods=['GET'])
def get_expected_features():
    """Return the expected input features and their descriptions."""
    feature_descriptions = {
        "Call Failure": "Number of call failures",
        "Subscription Length": "Length of subscription in months",
        "Charge Amount": "Monthly charge amount",
        "Seconds of Use": "Total seconds of usage",
        "Frequency of use": "Frequency of service usage",
        "Frequency of SMS": "SMS frequency",
        "Distinct Called Numbers": "Number of distinct numbers called",
        "Age Group": "Customer age group (1-5)",
        "Age": "Customer age in years",
        "Customer Value": "Customer value score",
        TARIFF_PLAN: "Tariff plan type (1 or 2)",
    }
    
    return jsonify({
        'required_features': feature_descriptions,
        'numerical_features': NUMERICAL_FEATURES,
        'categorical_features': CATEGORICAL_FEATURES,
        'example_payload': {
            "Call Failure": 0,
            "Subscription Length": 12,
            "Charge Amount": 50.25,
            "Seconds of Use": 1500,
            "Frequency of use": 25,
            "Frequency of SMS": 10,
            "Distinct Called Numbers": 15,
            "Age Group": 2,
            "Age": 35,
            "Customer Value": 1200.50,
            "Complains": 0,
            "Tariff Plan": 1,
            "Status": 1
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Detailed health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_status': 'loaded' if model is not None else 'not_loaded',
        'api_version': '1.0',
        'endpoints': ['/predict', '/features', '/health', '/']
    })

if __name__ == '__main__':
    print("🚀 Starting Iranian Churn Prediction API...")
    print("🔗 Available endpoints: /, /predict, /features, /health")
    app.run(host='0.0.0.0', port=5000, debug=True)
