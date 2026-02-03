"""
Order routes module
Handles order creation, retrieval, and status management
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions.db import db
from models.order import Order, OrderItem
from models.menu import MenuItem
from models.user import User
from utils.decorators import admin_required, validate_request_data

order_bp = Blueprint('orders', __name__)


@order_bp.route('', methods=['POST'])
@jwt_required()
@validate_request_data(['items'])
def create_order():
    """
    Create a new order

    Required JSON fields:
        - items: List of {menu_item_id, quantity}

    Optional fields:
        - delivery_address: Delivery address
        - notes: Order notes

    Returns:
        201: Order created successfully
        400: Validation error
        404: Menu item not found
    """
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        items_data = data.get('items', [])
        if not items_data or len(items_data) == 0:
            return jsonify({
                'error': 'empty_cart',
                'message': 'Order must contain at least one item'
            }), 400

        # Calculate total and validate items
        total_amount = 0
        order_items = []

        for item_data in items_data:
            if 'menu_item_id' not in item_data or 'quantity' not in item_data:
                return jsonify({
                    'error': 'invalid_item',
                    'message': 'Each item must have menu_item_id and quantity'
                }), 400

            menu_item = MenuItem.query.get(item_data['menu_item_id'])
            if not menu_item:
                return jsonify({
                    'error': 'item_not_found',
                    'message': f'Menu item {item_data["menu_item_id"]} not found'
                }), 404

            if not menu_item.available:
                return jsonify({
                    'error': 'item_unavailable',
                    'message': f'{menu_item.name} is currently unavailable'
                }), 400

            quantity = int(item_data['quantity'])
            if quantity < 1:
                return jsonify({
                    'error': 'invalid_quantity',
                    'message': 'Quantity must be at least 1'
                }), 400

            subtotal = menu_item.price * quantity
            total_amount += subtotal

            order_items.append({
                'menu_item_id': menu_item.id,
                'quantity': quantity,
                'price': menu_item.price
            })

        # Create order
        new_order = Order(
            user_id=current_user_id,
            total_amount=total_amount,
            delivery_address=data.get('delivery_address'),
            notes=data.get('notes'),
            order_mode=data.get('order_mode', 'Delivery'),
            payment_method=data.get('payment_method', 'Cash on Delivery'),
            status='PLACED'
        )

        db.session.add(new_order)
        db.session.flush()  # Get order ID without committing

        # Create order items
        for item_data in order_items:
            order_item = OrderItem(
                order_id=new_order.id,
                menu_item_id=item_data['menu_item_id'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            db.session.add(order_item)

        db.session.commit()

        return jsonify({
            'message': 'Order created successfully',
            'order': new_order.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'order_creation_failed',
            'message': str(e)
        }), 500


@order_bp.route('', methods=['GET'])
def get_user_orders_public():
    """
    Get orders - requires authentication
    If not authenticated, returns empty array

    Query parameters:
        - status: Filter by status (optional)

    Returns:
        200: List of user's orders or empty array
    """
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
    from flask_jwt_extended.exceptions import NoAuthorizationError

    try:
        # Try to get JWT token
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()

        if not current_user_id:
            # Not logged in - return empty array
            return jsonify({
                'orders': [],
                'count': 0
            }), 200

        query = Order.query.filter_by(user_id=current_user_id)

        # Apply status filter if provided
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)

        orders = query.order_by(Order.created_at.desc()).all()

        return jsonify({
            'orders': [order.to_dict() for order in orders],
            'count': len(orders)
        }), 200

    except Exception as e:
        # On any error, return empty array
        return jsonify({
            'orders': [],
            'count': 0
        }), 200


@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """
    Get a specific order by ID

    Returns:
        200: Order details
        403: Not authorized to view this order
        404: Order not found
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        order = Order.query.get(order_id)

        if not order:
            return jsonify({
                'error': 'order_not_found',
                'message': 'Order not found'
            }), 404

        # Users can only view their own orders unless they're admin
        if order.user_id != current_user_id and user.role != 'admin':
            return jsonify({
                'error': 'unauthorized',
                'message': 'Not authorized to view this order'
            }), 403

        return jsonify({
            'order': order.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'fetch_failed',
            'message': str(e)
        }), 500


@order_bp.route('/all', methods=['GET'])
@jwt_required()
@admin_required
def get_all_orders():
    """
    Get all orders (admin only)

    Query parameters:
        - status: Filter by status (optional)
        - user_id: Filter by user (optional)

    Returns:
        200: List of all orders
        403: Admin privileges required
    """
    try:
        query = Order.query

        # Apply filters
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)

        user_id = request.args.get('user_id')
        if user_id:
            query = query.filter_by(user_id=int(user_id))

        orders = query.order_by(Order.created_at.desc()).all()

        return jsonify({
            'orders': [order.to_dict() for order in orders],
            'count': len(orders)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'fetch_failed',
            'message': str(e)
        }), 500


@order_bp.route('/<int:order_id>/status', methods=['PATCH'])
@jwt_required()
@admin_required
@validate_request_data(['status'])
def update_order_status(order_id):
    """
    Update order status (admin only)

    Required JSON fields:
        - status: New status (pending, preparing, delivered, cancelled)

    Returns:
        200: Order status updated successfully
        400: Invalid status
        404: Order not found
        403: Admin privileges required
    """
    try:
        order = Order.query.get(order_id)

        if not order:
            return jsonify({
                'error': 'order_not_found',
                'message': 'Order not found'
            }), 404

        data = request.get_json()
        new_status = data['status']

        # Validate status
        valid_statuses = ['PLACED', 'PREPARING', 'OUT_FOR_DELIVERY', 'DELIVERED', 'CANCELLED']
        if new_status not in valid_statuses:
            return jsonify({
                'error': 'invalid_status',
                'message': f'Status must be one of: {", ".join(valid_statuses)}'
            }), 400

        order.status = new_status
        db.session.commit()

        return jsonify({
            'message': 'Order status updated successfully',
            'order': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'update_failed',
            'message': str(e)
        }), 500


@order_bp.route('/<int:order_id>', methods=['DELETE'])
@jwt_required()
def cancel_order(order_id):
    """
    Cancel an order (only if status is 'pending')

    Returns:
        200: Order cancelled successfully
        400: Order cannot be cancelled
        403: Not authorized
        404: Order not found
    """
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        order = Order.query.get(order_id)

        if not order:
            return jsonify({
                'error': 'order_not_found',
                'message': 'Order not found'
            }), 404

        # Users can only cancel their own orders unless they're admin
        if order.user_id != current_user_id and user.role != 'admin':
            return jsonify({
                'error': 'unauthorized',
                'message': 'Not authorized to cancel this order'
            }), 403

        # Only PLACED orders can be cancelled by users
        if order.status != 'PLACED' and user.role != 'admin':
            return jsonify({
                'error': 'cannot_cancel',
                'message': 'Only orders with PLACED status can be cancelled'
            }), 400

        order.status = 'CANCELLED'
        db.session.commit()

        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'cancellation_failed',
            'message': str(e)
        }), 500