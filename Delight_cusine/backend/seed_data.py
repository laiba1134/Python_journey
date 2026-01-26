"""
Seed data module
Contains functions to populate database with initial data
"""
from extensions.db import db
from models.menu import MenuItem
from models.user import User
from werkzeug.security import generate_password_hash


def seed_menu_items():
    """Seed database with initial menu items if empty"""

    # Check if menu items already exist
    if MenuItem.query.count() > 0:
        print("✓ Menu items already exist")
        return

    # Sample menu items
    menu_items = [
        # Appetizers
        MenuItem(
            name="Spring Rolls",
            description="Crispy vegetable spring rolls served with sweet chili sauce",
            price=5.99,
            category="appetizer",
            image_url="https://example.com/spring-rolls.jpg",
            available=True
        ),
        MenuItem(
            name="Chicken Wings",
            description="Spicy buffalo wings with blue cheese dip",
            price=8.99,
            category="appetizer",
            image_url="https://example.com/wings.jpg",
            available=True
        ),
        MenuItem(
            name="Garlic Bread",
            description="Toasted bread with garlic butter and herbs",
            price=4.99,
            category="appetizer",
            image_url="https://example.com/garlic-bread.jpg",
            available=True
        ),

        # Main Courses
        MenuItem(
            name="Margherita Pizza",
            description="Classic pizza with tomato sauce, mozzarella, and fresh basil",
            price=12.99,
            category="main",
            image_url="https://example.com/pizza.jpg",
            available=True
        ),
        MenuItem(
            name="Grilled Chicken Pasta",
            description="Penne pasta with grilled chicken in creamy alfredo sauce",
            price=14.99,
            category="main",
            image_url="https://example.com/pasta.jpg",
            available=True
        ),
        MenuItem(
            name="Beef Burger",
            description="Juicy beef patty with lettuce, tomato, and special sauce",
            price=11.99,
            category="main",
            image_url="https://example.com/burger.jpg",
            available=True
        ),
        MenuItem(
            name="Grilled Salmon",
            description="Fresh Atlantic salmon with lemon butter sauce",
            price=18.99,
            category="main",
            image_url="https://example.com/salmon.jpg",
            available=True
        ),
        MenuItem(
            name="Vegetable Stir Fry",
            description="Mixed vegetables in Asian-style sauce with rice",
            price=10.99,
            category="main",
            image_url="https://example.com/stir-fry.jpg",
            available=True
        ),

        # Desserts
        MenuItem(
            name="Chocolate Cake",
            description="Rich chocolate cake with vanilla ice cream",
            price=6.99,
            category="dessert",
            image_url="https://example.com/cake.jpg",
            available=True
        ),
        MenuItem(
            name="Tiramisu",
            description="Classic Italian dessert with coffee and mascarpone",
            price=7.99,
            category="dessert",
            image_url="https://example.com/tiramisu.jpg",
            available=True
        ),
        MenuItem(
            name="Cheesecake",
            description="New York style cheesecake with berry compote",
            price=7.49,
            category="dessert",
            image_url="https://example.com/cheesecake.jpg",
            available=True
        ),

        # Beverages
        MenuItem(
            name="Fresh Orange Juice",
            description="Freshly squeezed orange juice",
            price=3.99,
            category="beverage",
            image_url="https://example.com/orange-juice.jpg",
            available=True
        ),
        MenuItem(
            name="Iced Coffee",
            description="Cold brew coffee with ice and milk",
            price=4.99,
            category="beverage",
            image_url="https://example.com/iced-coffee.jpg",
            available=True
        ),
        MenuItem(
            name="Mango Smoothie",
            description="Fresh mango blended with yogurt and honey",
            price=5.49,
            category="beverage",
            image_url="https://example.com/smoothie.jpg",
            available=True
        ),
        MenuItem(
            name="Soft Drink",
            description="Choice of Coca-Cola, Sprite, or Fanta",
            price=2.99,
            category="beverage",
            image_url="https://example.com/soft-drink.jpg",
            available=True
        ),
    ]

    # Add all menu items to the session
    for item in menu_items:
        db.session.add(item)

    try:
        db.session.commit()
        print(f"✓ Successfully seeded {len(menu_items)} menu items")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error seeding menu items: {e}")


def create_default_admin():
    """Create default admin user if none exists"""

    admin = User.query.filter_by(email='admin@delightcuisine.com').first()
    if not admin:
        admin = User(
            email='admin@delightcuisine.com',
            password=generate_password_hash('admin123', method='pbkdf2:sha256'),
            name='Admin User',
            role='admin'
        )
        db.session.add(admin)
        try:
            db.session.commit()
            print("✓ Default admin user created (admin@delightcuisine.com / admin123)")
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error creating admin user: {e}")
    else:
        print("✓ Admin user already exists")


def seed_all():
    """Seed all initial data"""
    print("\n=== Seeding Database ===")
    create_default_admin()
    seed_menu_items()
    print("=== Seeding Complete ===\n")