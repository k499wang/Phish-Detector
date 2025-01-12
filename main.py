from app import create_app
from flask_cors import CORS
from waitress import serve

def main():
    app = create_app()
    # Use a production WSGI server (waitress) instead of Flask's development server
    serve(app, host="0.0.0.0", port=2222)

if __name__ == "__main__":
    main()