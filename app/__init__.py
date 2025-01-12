from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    
    CORS(app)

    
    from .routes.url_api import url_api
    app.register_blueprint(url_api)
    
    return app
    
    
    
    