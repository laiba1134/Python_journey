"""
Utility decorators module
Role-based access control and other custom decorators
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models.user import User

def admin_required(fn):
    """
    Decorator to ensure user has admin role
    Must be used after @jwt_required()

    Usage:
        @jwt_required()
        @admin_required
        def protected_route():
            pass
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({
                'error': 'user_not_found',
                'message': 'User not found'
            }), 404

        if user.role != 'admin':
            return jsonify({
                'error': 'admin_required',
                'message': 'Admin privileges required for this action'
            }), 403

        return fn(*args, **kwargs)

    return wrapper


def validate_request_data(required_fields):
    """
    Decorator to validate request JSON data contains required fields

    Args:
        required_fields: List of field names that must be present

    Usage:
        @validate_request_data(['email', 'password'])
        def login():
            pass
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from flask import request

            if not request.is_json:
                return jsonify({
                    'error': 'invalid_request',
                    'message': 'Request must be JSON'
                }), 400

            data = request.get_json()
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return jsonify({
                    'error': 'missing_fields',
                    'message': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400

            return fn(*args, **kwargs)

        return wrapper
    return decorator