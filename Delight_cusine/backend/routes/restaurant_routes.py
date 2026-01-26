"""
Restaurant routes module
Handles restaurant status management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions.db import db
from utils.decorators import admin_required

restaurant_bp = Blueprint('restaurant', __name__)

# Simple in-memory storage for restaurant status (you can move to DB later)
restaurant_status = {'is_open': True}


@restaurant_bp.route('/status', methods=['GET'])
def get_status():
    """
    Get restaurant open/closed status

    Returns:
        200: Restaurant status
    """
    return jsonify({
        'is_open': restaurant_status['is_open']
    }), 200


@restaurant_bp.route('/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_status():
    """
    Update restaurant open/closed status (admin only)

    Required JSON fields:
        - is_open: Boolean status

    Returns:
        200: Status updated successfully
        403: Admin privileges required
    """
    try:
        data = request.get_json()

        if 'is_open' not in data:
            return jsonify({
                'error': 'missing_field',
                'message': 'is_open field is required'
            }), 400

        restaurant_status['is_open'] = bool(data['is_open'])

        return jsonify({
            'message': 'Restaurant status updated successfully',
            'is_open': restaurant_status['is_open']
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'update_failed',
            'message': str(e)
        }), 500