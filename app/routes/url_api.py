from flask import Blueprint, request, jsonify
import joblib
import numpy as np

url_api = Blueprint('url_api', __name__)

model = joblib.load('logistic_model.pkl')

@url_api.route('/predict_url', methods=['POST'])
def predict_url():
    return jsonify({
        'hello': 'world'
    })