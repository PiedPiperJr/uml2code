import os
import sys
from flask import Flask
from flask_cors import CORS
from routes.routes import bp as routes_bp
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'services', 'code_generator_service')))

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(routes_bp)
    return app

app = create_app() 
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")