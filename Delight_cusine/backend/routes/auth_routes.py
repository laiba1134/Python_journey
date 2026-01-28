"""
Authentication routes module
Handles user registration, login, and JWT token management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,  # ADD THIS LINE
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from extensions.db import db
from models.user import User
from utils.decorators import validate_request_data

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@validate_request_data(['email', 'password', 'name'])
def register():
    """
    Register a new user
    """
    try:
        data = request.get_json()

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'error': 'user_exists',
                'message': 'User with this email already exists'
            }), 409

        # Create new user
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(
            email=data['email'],
            password=hashed_password,
            name=data['name'],
            role='customer'
        )

        db.session.add(new_user)
        db.session.commit()

        # Generate both tokens
        access_token = create_access_token(identity=new_user.id)
        refresh_token = create_refresh_token(identity=new_user.id)

        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'registration_failed',
            'message': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
@validate_request_data(['email', 'password'])
def login():
    """
    Authenticate user and return JWT tokens
    """
    try:
        data = request.get_json()

        # Find user
        user = User.query.filter_by(email=data['email']).first()

        # Verify user and password
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({
                'error': 'invalid_credentials',
                'message': 'Invalid email or password'
            }), 401

        # Generate both access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'login_failed',
            'message': str(e)
        }), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token

    Returns:
        200: New access token
        401: Invalid refresh token
    """
    try:
        current_user_id = get_jwt_identity()

        # Generate new access token
        access_token = create_access_token(identity=current_user_id)

        return jsonify({
            'access_token': access_token
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'refresh_failed',
            'message': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user's information
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({
                'error': 'user_not_found',
                'message': 'User not found'
            }), 404

        return jsonify({
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'fetch_failed',
            'message': str(e)
        }), 500