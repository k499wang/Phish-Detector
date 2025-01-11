from app import create_app
from flask_cors import CORS


def main():
    app = create_app()


    app.run(debug=True)

main()