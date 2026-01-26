"""
JWT extension module
JWT manager initialization and configuration
"""
from flask_jwt_extended import JWTManager

jwt = JWTManager()

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired token"""
    return {
        'error': 'token_expired',
        'message': 'The token has expired'
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid token"""
    return {
        'error': 'invalid_token',
        'message': 'Signature verification failed'
    }, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing token"""
    return {
        'error': 'authorization_required',
        'message': 'Request does not contain an access token'
    }, 401