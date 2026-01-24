from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Float, Boolean, Integer, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from passlib.context import CryptContext
import enum

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./delight_cuisine.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============= ENUMS =============
class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class OrderStatus(str, enum.Enum):
    PLACED = "placed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"

class OrderMode(str, enum.Enum):
    DINE_IN = "dine_in"
    TAKEAWAY = "takeaway"
    DELIVERY = "delivery"

# ============= DATABASE MODELS =============
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.CUSTOMER)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String)
    available = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    total = Column(Float, nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PLACED)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    order_mode = Column(SQLEnum(OrderMode), nullable=False)
    timestamp = Column(String, nullable=False)
    items_json = Column(String, nullable=False)  # Store items as JSON string

    user = relationship("User", back_populates="orders")

class RestaurantStatus(Base):
    __tablename__ = "restaurant_status"

    id = Column(Integer, primary_key=True)
    is_open = Column(Boolean, default=True)

# Create tables
Base.metadata.create_all(bind=engine)

# ============= PYDANTIC SCHEMAS =============
class LoginRequest(BaseModel):
    username: str
    password: str
    requested_role: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.CUSTOMER

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    createdAt: str

    class Config:
        from_attributes = True

class MenuItemSchema(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    image: str
    available: bool = True
    is_deleted: bool = False

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    image: Optional[str] = None
    available: Optional[bool] = None
    is_deleted: Optional[bool] = None

class OrderCreate(BaseModel):
    user_id: str
    items: List[dict]
    total: float
    status: OrderStatus = OrderStatus.PLACED
    payment_method: PaymentMethod
    order_mode: OrderMode

class OrderResponse(BaseModel):
    id: str
    user_id: str
    total: float
    status: str
    payment_method: str
    order_mode: str
    timestamp: str
    items: List[dict]

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class RestaurantStatusSchema(BaseModel):
    is_open: bool

# ============= DEPENDENCY =============
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============= SEED DATA =============
def seed_database():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(User).count() > 0:
            return

        # Create admin user
        admin = User(
            id="admin_001",
            username="admin",
            email="admin@delightcuisine.com",
            hashed_password=pwd_context.hash("admin123"),
            role=UserRole.ADMIN
        )
        db.add(admin)

        # Create menu items
        menu_items = [
            MenuItem(
                id="item_001",
                name="Delight Truffle Burger",
                description="Double beef patty, truffle mayo, and a drizzle of spicy honey.",
                price=18.50,
                category="BURGERS",
                image="https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
                available=True
            ),
            MenuItem(
                id="item_002",
                name="Golden Glazed Wings",
                description="Crispy wings tossed in a signature honey-soy glaze.",
                price=12.00,
                category="APPETIZERS",
                image="https://images.unsplash.com/photo-1608039829572-78524f79c4c7",
                available=True
            ),
            MenuItem(
                id="item_003",
                name="Seasonal Root Salad",
                description="Seasonal vegetables, goat cheese, and honey balsamic vinaigrette.",
                price=14.50,
                category="SALADS",
                image="https://images.unsplash.com/photo-1546793665-c74683f339c1",
                available=True
            ),
            MenuItem(
                id="item_004",
                name="Spicy Delight Pizza",
                description="Hot salami, mozzarella, and a generous honey swirl.",
                price=21.00,
                category="MAIN COURSES",
                image="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38",
                available=True
            ),
            MenuItem(
                id="item_005",
                name="Honey Pancake Stack",
                description="Fluffy pancakes with butter, honey drizzle, and fresh berries.",
                price=13.00,
                category="BREAKFAST",
                image="https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445",
                available=True
            ),
            MenuItem(
                id="item_006",
                name="Chocolate Lava Cake",
                description="Rich chocolate cake with a molten center and vanilla ice cream.",
                price=9.50,
                category="DESSERTS",
                image="https://images.unsplash.com/photo-1578985545062-69928b1d9587",
                available=True
            ),
        ]

        for item in menu_items:
            db.add(item)

        # Create restaurant status
        status = RestaurantStatus(is_open=True)
        db.add(status)

        db.commit()
        print("✅ Database seeded successfully!")
        print("Admin credentials: username=admin, password=admin123")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

# ============= FASTAPI APP =============
app = FastAPI(title="Delight Cuisine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed database on startup
@app.on_event("startup")
def startup_event():
    seed_database()

# ============= AUTH ENDPOINTS =============
@app.post("/api/auth/login", response_model=UserResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.email == credentials.username) | (User.username == credentials.username)
    ).first()

    if not user or not pwd_context.verify(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email/username or password")

    if credentials.requested_role and user.role.value != credentials.requested_role:
        raise HTTPException(status_code=403, detail=f"Access denied. This account is not authorized for {credentials.requested_role} access.")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role.value,
        createdAt=user.created_at.isoformat()
    )

@app.post("/api/auth/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        id=f"user_{int(datetime.now().timestamp())}",
        username=user_data.username,
        email=user_data.email,
        hashed_password=pwd_context.hash(user_data.password),
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        role=new_user.role.value,
        createdAt=new_user.created_at.isoformat()
    )

# ============= MENU ENDPOINTS =============
@app.get("/api/menu", response_model=List[MenuItemSchema])
def get_menu(db: Session = Depends(get_db)):
    items = db.query(MenuItem).all()
    return items

@app.post("/api/menu", response_model=MenuItemSchema)
def create_menu_item(item: MenuItemSchema, db: Session = Depends(get_db)):
    new_item = MenuItem(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.put("/api/menu/{item_id}", response_model=MenuItemSchema)
def update_menu_item(item_id: str, item: MenuItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/api/menu/batch")
def batch_update_menu_items(items: List[dict], db: Session = Depends(get_db)):
    """Batch update multiple menu items - accepts raw dict to avoid validation issues"""
    try:
        print(f"\n{'='*50}")
        print(f"📥 Received {len(items)} items for batch update")
        print(f"📋 First item structure: {items[0] if items else 'none'}")

        updated_count = 0
        for item_data in items:
            item_id = item_data.get('id')
            db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()

            if db_item:
                # Update existing item
                db_item.name = item_data.get('name', db_item.name)
                db_item.description = item_data.get('description', db_item.description)
                db_item.price = item_data.get('price', db_item.price)
                db_item.category = item_data.get('category', db_item.category)
                db_item.image = item_data.get('image', db_item.image)
                db_item.available = item_data.get('available', db_item.available)
                db_item.is_deleted = item_data.get('is_deleted', db_item.is_deleted)

                print(f"✏️ Updated item {item_id}: is_deleted={db_item.is_deleted}, name={db_item.name}")
                updated_count += 1
            else:
                # Create new item
                new_item = MenuItem(
                    id=item_data.get('id'),
                    name=item_data.get('name'),
                    description=item_data.get('description'),
                    price=item_data.get('price'),
                    category=item_data.get('category'),
                    image=item_data.get('image'),
                    available=item_data.get('available', True),
                    is_deleted=item_data.get('is_deleted', False)
                )
                db.add(new_item)
                print(f"➕ Created new item {item_id}")
                updated_count += 1

        db.commit()
        print(f"✅ Successfully committed {updated_count} items to database")

        # Verify the data was saved
        if items:
            verification = db.query(MenuItem).filter(MenuItem.id == items[0].get('id')).first()
            if verification:
                print(f"🔍 Verification - Item {verification.id}: is_deleted={verification.is_deleted}")

        print(f"{'='*50}\n")

        return {"message": "Menu updated successfully", "count": len(items)}
    except Exception as e:
        print(f"❌ Error in batch update: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.patch("/api/menu/{item_id}/toggle")
def toggle_item_availability(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db_item.available = not db_item.available
    db.commit()
    return {"message": "Item availability toggled", "available": db_item.available}

# ============= ORDER ENDPOINTS =============
@app.get("/api/orders")
def get_orders(user_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Order)
    if user_id:
        query = query.filter(Order.user_id == user_id)

    orders = query.order_by(Order.timestamp.desc()).all()

    result = []
    for order in orders:
        import json
        result.append({
            "id": order.id,
            "user_id": order.user_id,
            "total": order.total,
            "status": order.status.value,
            "payment_method": order.payment_method.value,
            "order_mode": order.order_mode.value,
            "timestamp": order.timestamp,
            "items": json.loads(order.items_json)
        })

    return result

@app.post("/api/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    import json

    new_order = Order(
        id=datetime.now().strftime("%Y%m%d%H%M%S"),
        user_id=order.user_id,
        total=order.total,
        status=order.status,
        payment_method=order.payment_method,
        order_mode=order.order_mode,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        items_json=json.dumps(order.items)
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "id": new_order.id,
        "user_id": new_order.user_id,
        "total": new_order.total,
        "status": new_order.status.value,
        "payment_method": new_order.payment_method.value,
        "order_mode": new_order.order_mode.value,
        "timestamp": new_order.timestamp,
        "items": json.loads(new_order.items_json)
    }

@app.patch("/api/orders/{order_id}/status")
def update_order_status(order_id: str, status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status_update.status
    db.commit()
    return {"message": "Order status updated", "status": order.status.value}

# ============= RESTAURANT STATUS =============
@app.get("/api/restaurant/status")
def get_restaurant_status(db: Session = Depends(get_db)):
    status = db.query(RestaurantStatus).first()
    if not status:
        status = RestaurantStatus(is_open=True)
        db.add(status)
        db.commit()
    return {"is_open": status.is_open}

@app.put("/api/restaurant/status")
def update_restaurant_status(status_update: RestaurantStatusSchema, db: Session = Depends(get_db)):
    status = db.query(RestaurantStatus).first()
    if not status:
        status = RestaurantStatus(is_open=status_update.is_open)
        db.add(status)
    else:
        status.is_open = status_update.is_open

    db.commit()
    return {"message": "Restaurant status updated", "is_open": status.is_open}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)