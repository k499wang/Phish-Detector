from flask import Blueprint, request, jsonify
from ..utils.extract_features import return_features
import joblib

import numpy as np

url_api = Blueprint('url_api', __name__)

model = joblib.load('logistic_model.pkl')

@url_api.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Hello, World!'})

@url_api.route('/predict_url', methods=['POST', 'GET'])
def predict_url():
    
    url = request.json.get('url', None)
    
 
    if url is None:
        return jsonify({'error': 'No URL provided'})
    
    features = return_features(url)
    
    if features is False:
        return jsonify({'error': 'Invalid URL'})
    
    features = np.array(features).reshape(1, -1)
    
    prediction = model.predict(features)
    probability = model.predict_proba(features)
    
    return jsonify({'prediction': int(prediction[0]), 'probability': float(probability[0][0])})