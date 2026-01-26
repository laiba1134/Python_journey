"""
Delight Cuisine - Flask Backend Application
Main application entry point
"""
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from extensions.db import db
from extensions.jwt import jwt
from routes.auth_routes import auth_bp
from routes.menu_routes import menu_bp
from routes.order_routes import order_bp
from config.config import Config

# Load environment variables
load_dotenv()

def create_app(config_class=Config):
    """
    Flask application factory

    Args:
        config_class: Configuration class to use

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(menu_bp, url_prefix='/api/menu')
    app.register_blueprint(order_bp, url_prefix='/api/orders')

    # Create database tables
    with app.app_context():
        db.create_all()
        _create_default_admin()

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return {'status': 'healthy', 'service': 'Delight Cuisine API'}, 200

    return app

def _create_default_admin():
    """Create default admin user if none exists"""
    from models.user import User
    from werkzeug.security import generate_password_hash

    admin = User.query.filter_by(email='admin@delightcuisine.com').first()
    if not admin:
        admin = User(
            email='admin@delightcuisine.com',
            password=generate_password_hash('admin123', method='pbkdf2:sha256'),
            name='Admin User',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Default admin user created (admin@delightcuisine.com / admin123)")

if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )