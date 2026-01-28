"""
Routes package
Exports all route blueprints
"""
from routes.auth_routes import auth_bp
from routes.menu_routes import menu_bp
from routes.order_routes import order_bp
from routes.restaurant_routes import restaurant_bp

__all__ = ['auth_bp', 'menu_bp', 'order_bp', 'restaurant_bp']