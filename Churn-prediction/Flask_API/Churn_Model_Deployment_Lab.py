# Implement model using Flask
from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('Optimized_IRN_churn_prediction_model.pkl')

# Define the prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    input_data = pd.DataFrame([data])
    prediction = model.predict(input_data)
    return jsonify({'churn_prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)
