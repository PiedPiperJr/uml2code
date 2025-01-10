from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    return app