"""
User model module
Defines user entity with authentication capabilities
"""
from extensions.db import db
from datetime import datetime

class User(db.Model):
    """User model for authentication and authorization"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer')  # 'admin' or 'customer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_orders=False):
        """
        Convert user object to dictionary

        Args:
            include_orders: Whether to include user's orders

        Returns:
            Dictionary representation of user (excludes password)
        """
        data = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }

        if include_orders:
            data['orders'] = [order.to_dict() for order in self.orders]

        return data

    def __repr__(self):
        return f'<User {self.email}>'