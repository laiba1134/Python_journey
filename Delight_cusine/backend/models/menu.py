"""
Menu model module
Defines menu item entity
"""
from extensions.db import db
from datetime import datetime

class MenuItem(db.Model):
    """Menu item model"""

    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # e.g., 'appetizer', 'main', 'dessert', 'beverage'
    image_url = db.Column(db.String(255))
    available = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)  # Soft delete flag
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        Convert menu item to dictionary

        Returns:
            Dictionary representation of menu item
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url,
            'available': self.available,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<MenuItem {self.name}>'