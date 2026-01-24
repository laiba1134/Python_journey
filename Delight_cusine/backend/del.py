from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///./delight_cuisine.db")
with engine.connect() as conn:
    result = conn.execute(text("SELECT id, name, is_deleted FROM menu_items"))
    for row in result:
        print(f"{row[0]}: {row[1]} - is_deleted={row[2]}")
        