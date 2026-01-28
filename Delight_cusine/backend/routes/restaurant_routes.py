"""
Restaurant routes module
Handles restaurant status and settings management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions.db import db
from utils.decorators import admin_required

restaurant_bp = Blueprint('restaurant', __name__)

# In-memory storage for restaurant status (for simplicity)
# In production, this would be stored in database
restaurant_status = {
    'is_open': True,
    'message': 'We are currently accepting orders!'
}


@restaurant_bp.route('/status', methods=['GET'])
def get_status():
    """
    Get restaurant status (public endpoint)

    Returns:
        200: Restaurant status
    """
    return jsonify({
        'isOpen': restaurant_status['is_open'],
        'message': restaurant_status['message']
    }), 200


@restaurant_bp.route('/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_status():
    """
    Update restaurant status (admin only)

    Optional JSON fields:
        - is_open: Boolean indicating if restaurant is accepting orders
        - message: Status message

    Returns:
        200: Status updated successfully
        403: Admin privileges required
    """
    try:
        data = request.get_json() or {}

        if 'is_open' in data:
            restaurant_status['is_open'] = bool(data['is_open'])

        if 'message' in data:
            restaurant_status['message'] = data['message']

        return jsonify({
            'message': 'Restaurant status updated successfully',
            'status': {
                'isOpen': restaurant_status['is_open'],
                'message': restaurant_status['message']
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'update_failed',
            'message': str(e)
        }), 500


@restaurant_bp.route('/toggle', methods=['POST'])
@jwt_required()
@admin_required
def toggle_status():
    """
    Toggle restaurant open/closed status (admin only)

    Returns:
        200: Status toggled successfully
        403: Admin privileges required
    """
    try:
        restaurant_status['is_open'] = not restaurant_status['is_open']

        # Update message based on status
        restaurant_status['message'] = (
            'We are currently accepting orders!' if restaurant_status['is_open']
            else 'We are currently closed. Please check back later!'
        )

        return jsonify({
            'message': 'Restaurant status toggled successfully',
            'status': {
                'isOpen': restaurant_status['is_open'],
                'message': restaurant_status['message']
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'toggle_failed',
            'message': str(e)
        }), 500