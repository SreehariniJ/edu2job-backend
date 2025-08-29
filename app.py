from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Basic config
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///edu2job.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Init extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)  # allow all origins for now; update later

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.prediction_routes import pred_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(pred_bp, url_prefix='/predict')

    # Optional root test
    @app.route('/')
    def index():
        return jsonify({"status":"backend running"})

    return app

# Top-level app variable for Gunicorn
app = create_app()

# Run locally if executed directly
if __name__ == "__main__":
    app.run(debug=True)
