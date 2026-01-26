"""
Migration script to add is_deleted column to existing menu_items table
"""
from app import create_app
from extensions.db import db

def add_is_deleted_column():
    app = create_app()
    with app.app_context():
        try:
            # Add the is_deleted column with default value False
            db.engine.execute("""
                ALTER TABLE menu_items
                ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE
            """)
            print("✓ Successfully added is_deleted column to menu_items table")
        except Exception as e:
            print(f"✗ Error adding column: {e}")
            print("Note: If column already exists, this is expected.")

if __name__ == '__main__':
    add_is_deleted_column()