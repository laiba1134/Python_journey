"""
Menu routes module
Handles menu item CRUD operations
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions.db import db
from models.menu import MenuItem
from utils.decorators import admin_required, validate_request_data

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('', methods=['GET'])
def get_menu_items():
    """
    Get all menu items (public endpoint)
    By default, only shows non-deleted items
    Admin can request deleted items with include_deleted=true

    Query parameters:
        - category: Filter by category (optional)
        - available: Filter by availability (optional, true/false)
        - include_deleted: Include soft-deleted items (optional, admin only)

    Returns:
        200: List of menu items
    """
    try:
        # Start with base query - exclude deleted items by default
        query = MenuItem.query.filter_by(is_deleted=False)

        # Admin can request to see deleted items
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        if include_deleted:
            query = MenuItem.query  # Show all items including deleted

        # Apply filters
        category = request.args.get('category')
        if category:
            query = query.filter_by(category=category)

        available = request.args.get('available')
        if available is not None:
            available_bool = available.lower() == 'true'
            query = query.filter_by(available=available_bool)

        menu_items = query.all()

        return jsonify({
            'menu_items': [item.to_dict() for item in menu_items],
            'count': len(menu_items)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'fetch_failed',
            'message': str(e)
        }), 500


@menu_bp.route('/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    """
    Get a specific menu item by ID

    Returns:
        200: Menu item details
        404: Menu item not found
    """
    try:
        menu_item = MenuItem.query.filter_by(id=item_id, is_deleted=False).first()

        if not menu_item:
            return jsonify({
                'error': 'item_not_found',
                'message': 'Menu item not found'
            }), 404

        return jsonify({
            'menu_item': menu_item.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'fetch_failed',
            'message': str(e)
        }), 500


@menu_bp.route('', methods=['POST'])
@jwt_required()
@admin_required
@validate_request_data(['name', 'price', 'category'])
def create_menu_item():
    """
    Create a new menu item (admin only)

    Required JSON fields:
        - name: Item name
        - price: Item price
        - category: Item category

    Optional fields:
        - description: Item description
        - image_url: URL to item image
        - available: Availability status (default: true)

    Returns:
        201: Menu item created successfully
        400: Validation error
        403: Admin privileges required
    """
    try:
        data = request.get_json()

        # Validate price
        try:
            price = float(data['price'])
            if price < 0:
                return jsonify({
                    'error': 'invalid_price',
                    'message': 'Price must be non-negative'
                }), 400
        except ValueError:
            return jsonify({
                'error': 'invalid_price',
                'message': 'Price must be a valid number'
            }), 400

        new_item = MenuItem(
            name=data['name'],
            description=data.get('description'),
            price=price,
            category=data['category'],
            image_url=data.get('image_url'),
            available=data.get('available', True),
            is_deleted=False
        )

        db.session.add(new_item)
        db.session.commit()

        return jsonify({
            'message': 'Menu item created successfully',
            'menu_item': new_item.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'creation_failed',
            'message': str(e)
        }), 500


@menu_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_menu_item(item_id):
    """
    Update an existing menu item (admin only)

    Accepts any combination of fields to update

    Returns:
        200: Menu item updated successfully
        404: Menu item not found
        403: Admin privileges required
    """
    try:
        menu_item = MenuItem.query.get(item_id)

        if not menu_item:
            return jsonify({
                'error': 'item_not_found',
                'message': 'Menu item not found'
            }), 404

        data = request.get_json()

        # Update fields if provided
        if 'name' in data:
            menu_item.name = data['name']
        if 'description' in data:
            menu_item.description = data['description']
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    return jsonify({
                        'error': 'invalid_price',
                        'message': 'Price must be non-negative'
                    }), 400
                menu_item.price = price
            except ValueError:
                return jsonify({
                    'error': 'invalid_price',
                    'message': 'Price must be a valid number'
                }), 400
        if 'category' in data:
            menu_item.category = data['category']
        if 'image_url' in data:
            menu_item.image_url = data['image_url']
        if 'available' in data:
            menu_item.available = data['available']

        db.session.commit()

        return jsonify({
            'message': 'Menu item updated successfully',
            'menu_item': menu_item.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'update_failed',
            'message': str(e)
        }), 500


@menu_bp.route('/<int:item_id>/toggle', methods=['PATCH'])
@jwt_required()
@admin_required
def toggle_item_availability(item_id):
    """
    Toggle menu item availability (admin only)
    This is separate from restaurant status - allows marking specific items as sold out

    Returns:
        200: Availability toggled successfully
        404: Menu item not found
        403: Admin privileges required
    """
    try:
        menu_item = MenuItem.query.filter_by(id=item_id, is_deleted=False).first()

        if not menu_item:
            return jsonify({
                'error': 'item_not_found',
                'message': 'Menu item not found'
            }), 404

        menu_item.available = not menu_item.available
        db.session.commit()

        return jsonify({
            'message': f'Item {"enabled" if menu_item.available else "disabled"} successfully',
            'menu_item': menu_item.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'toggle_failed',
            'message': str(e)
        }), 500


@menu_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_menu_item(item_id):
    """
    Soft delete a menu item (admin only)
    Item is marked as deleted but kept in database for history

    Returns:
        200: Menu item deleted successfully
        404: Menu item not found
        403: Admin privileges required
    """
    try:
        menu_item = MenuItem.query.get(item_id)

        if not menu_item:
            return jsonify({
                'error': 'item_not_found',
                'message': 'Menu item not found'
            }), 404

        # Soft delete - mark as deleted instead of removing from database
        menu_item.is_deleted = True
        db.session.commit()

        return jsonify({
            'message': 'Menu item deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'deletion_failed',
            'message': str(e)
        }), 500


@menu_bp.route('/<int:item_id>/restore', methods=['PATCH'])
@jwt_required()
@admin_required
def restore_menu_item(item_id):
    """
    Restore a soft-deleted menu item (admin only)

    Returns:
        200: Menu item restored successfully
        404: Menu item not found
        403: Admin privileges required
    """
    try:
        menu_item = MenuItem.query.filter_by(id=item_id, is_deleted=True).first()

        if not menu_item:
            return jsonify({
                'error': 'item_not_found',
                'message': 'Deleted menu item not found'
            }), 404

        menu_item.is_deleted = False
        db.session.commit()

        return jsonify({
            'message': 'Menu item restored successfully',
            'menu_item': menu_item.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'restore_failed',
            'message': str(e)
        }), 500


@menu_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all unique menu categories (only from non-deleted items)

    Returns:
        200: List of categories
    """
    try:
        categories = db.session.query(MenuItem.category).filter_by(is_deleted=False).distinct().all()
        category_list = [cat[0] for cat in categories]

        return jsonify({
            'categories': category_list,
            'count': len(category_list)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'fetch_failed',
            'message': str(e)
        }), 500