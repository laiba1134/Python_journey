"""
Migration script to add is_deleted column to existing menu_items table
"""
from app import create_app
from extensions.db import db

def add_is_deleted_column():
    app = create_app()
    with app.app_context():
        try:
            # Check if column already exists
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('menu_items')]

            if 'is_deleted' in columns:
                print("✓ is_deleted column already exists")
                return

            # Add the is_deleted column with default value False
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    ALTER TABLE menu_items
                    ADD COLUMN is_deleted BOOLEAN DEFAULT 0
                """))
                conn.commit()

            print("✓ Successfully added is_deleted column to menu_items table")
        except Exception as e:
            print(f"✗ Error adding column: {e}")

if __name__ == '__main__':
    add_is_deleted_column()