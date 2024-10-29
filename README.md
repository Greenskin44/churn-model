# Churn Prediction Model

This repository contains a machine learning model designed to predict 
customer churn in an Iranian telecom company. 
The project includes model training, evaluation, deployment via Docker, 
and a REST API for serving predictions.

## Table of Contents
1. - [Installation](#installation)
2. - [Usage](#usage)
3. - [Model Explainability](#model-explainability)
4. - [Docker Instructions](#docker-instructions)
5. - [API Instructions](#api-instructions)
6. - [CI/CD Pipeline](#cicd-pipeline)
7. - [License](#license)

---

## Installation

To set up this project locally, follow these steps:

1. **Clone the repository:**
      ```bash/terminal
       git clone https://github.com/Greenskin44/churn-prediction.git
       cd churn-prediction


2. **Usage**
  a. Train and Evaluate the Model To train and evaluate the model, use:
     Iranian Churn Prediction Model.ipynb
     import joblib
     
  b. Model Inference For predictions using the saved model:
    import joblib
    model = joblib.load('Optimized_IRN_churn_prediction_model.pkl')
    predictions = model.predict(X_test)
  
c. Model Explanation Use LIME for explainability on a single instance
    or SHAP (if supported):
    from lime import lime_tabular
    explainer = lime_tabular.LimeTabularExplainer(...)
    explanation = explainer.explain_instance(X_test.iloc[0],           
    model.predict_proba)


3. **Model Explainability**
   ```a. LIME (Local Interpretable Model-agnostic Explanations) has been implemented for feature importance. To explain a specific prediction, use:
   from lime import lime_tabular
   explainer = lime_tabular.LimeTabularExplainer(...)
   explanation = explainer.explain_instance(X_test.iloc[0],model.predict_proba)
   explanation.show_in_notebook()

5. ***Docker Deployment***
   a. This project includes Docker setup for consistent deployment. For full Docker instructions, see Docker/README.md.
      ```b. Basic Docker Commands:
         docker build -t churn-model .
         docker run -p 5000:5000 churn-model

7. API Instructions
  a. The API exposes a /predict endpoint for making predictions. Detailed API usage can be found in API/README.md.
   ```b. Run API Locally:
      python app.py
  c. API Endpoint:
POST /predict for prediction with JSON data input.

9. CI/CD Pipeline
   a. We use GitHub Actions for continuous integration and deployment. For details on the CI/CD setup, see .github/README.md.

10. License
   a. This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

  
