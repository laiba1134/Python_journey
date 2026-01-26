"""
Order model module
Defines order and order item entities
"""
from extensions.db import db
from datetime import datetime

class Order(db.Model):
    """Order model"""

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='PLACED')  # 'PLACED', 'PREPARING', 'OUT_FOR_DELIVERY', 'DELIVERED', 'CANCELLED'
    total_amount = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.Text)
    notes = db.Column(db.Text)
    order_mode = db.Column(db.String(50), default='Delivery')  # 'Delivery' or 'Pickup'
    payment_method = db.Column(db.String(50), default='Cash on Delivery')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_items=True):
        """
        Convert order to dictionary

        Args:
            include_items: Whether to include order items

        Returns:
            Dictionary representation of order (frontend-compatible format)
        """
        data = {
            'id': str(self.id),  # Convert to string for frontend
            'user_id': self.user_id,
            'status': self.status,
            'total': self.total_amount,  # Frontend expects 'total' not 'total_amount'
            'delivery_address': self.delivery_address,
            'notes': self.notes,
            'timestamp': self.created_at.strftime('%Y-%m-%d %H:%M'),  # Formatted timestamp
            'orderMode': self.order_mode,  # camelCase for frontend
            'paymentMethod': self.payment_method,  # camelCase for frontend
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        if include_items:
            data['items'] = [item.to_dict() for item in self.items]

        return data

    def __repr__(self):
        return f'<Order {self.id}>'


class OrderItem(db.Model):
    """Order item model - represents individual items in an order"""

    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)  # Price at time of order

    # Relationships
    menu_item = db.relationship('MenuItem', backref='order_items')

    def to_dict(self):
        """
        Convert order item to dictionary

        Returns:
            Dictionary representation of order item (frontend-compatible format)
        """
        return {
            'id': str(self.id),  # Convert to string for frontend
            'order_id': self.order_id,
            'quantity': self.quantity,
            'menuItem': {  # Nested object for frontend
                'id': self.menu_item_id,
                'name': self.menu_item.name if self.menu_item else 'Unknown Item',
                'price': self.price
            }
        }

    def __repr__(self):
        return f'<OrderItem {self.id}>'