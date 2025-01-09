from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from routes import url_api
    app.register_blueprint(url_api)
    
    return app
    
    
    
    