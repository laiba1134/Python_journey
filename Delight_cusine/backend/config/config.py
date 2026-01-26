"""
Application configuration module
Loads environment variables and configures Flask app
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""

    # Flask Core
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///delight_cuisine.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = FLASK_ENV == 'development'

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-please-change')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    )
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # API Configuration
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = FLASK_ENV == 'development'