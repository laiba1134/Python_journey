from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import os
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============= ENUMS =============

class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"

class OrderStatus(str, Enum):
    PLACED = "placed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"

class OrderMode(str, Enum):
    DINE_IN = "dine_in"
    TAKEAWAY = "takeaway"
    DELIVERY = "delivery"

# ============= SCHEMAS =============

class LoginRequest(BaseModel):
    username: str
    password: str
    requested_role: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.CUSTOMER

class User(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str
    role: UserRole
    created_at: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: UserRole
    created_at: str

class MenuItem(BaseModel):
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

class OrderItem(BaseModel):
    id: str
    menu_item_id: str
    quantity: int
    price_at_time: float

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]
    total: float
    status: OrderStatus = OrderStatus.PLACED
    payment_method: PaymentMethod
    order_mode: OrderMode

class Order(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    total: float
    status: OrderStatus
    payment_method: PaymentMethod
    order_mode: OrderMode
    timestamp: str

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class RestaurantStatus(BaseModel):
    is_open: bool

# ============= JSON FILE MANAGER =============

class JSONFileManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

        self.users_file = os.path.join(data_dir, "users.json")
        self.menu_file = os.path.join(data_dir, "menu.json")
        self.orders_file = os.path.join(data_dir, "orders.json")
        self.status_file = os.path.join(data_dir, "restaurant_status.json")

        self._initialize_files()

    def _initialize_files(self):
        # Initialize users file with only admin
        if not os.path.exists(self.users_file):
            default_users = [
                {
                    "id": "admin_001",
                    "username": "admin",
                    "email": "admin@delightcuisine.com",
                    "hashed_password": pwd_context.hash("admin123"),
                    "role": "admin",
                    "created_at": datetime.now().isoformat()
                }
            ]
            self._write_json(self.users_file, default_users)

        # Initialize menu file
        if not os.path.exists(self.menu_file):
            default_menu = [
                {
                    "id": "item_001",
                    "name": "Margherita Pizza",
                    "description": "Classic pizza with fresh mozzarella and basil",
                    "price": 12.99,
                    "category": "Pizza",
                    "image": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002",
                    "available": True,
                    "is_deleted": False
                },
                {
                    "id": "item_002",
                    "name": "Beef Burger",
                    "description": "Juicy beef patty with cheese and special sauce",
                    "price": 10.99,
                    "category": "Burgers",
                    "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
                    "available": True,
                    "is_deleted": False
                },
                {
                    "id": "item_003",
                    "name": "Caesar Salad",
                    "description": "Fresh romaine lettuce with parmesan and croutons",
                    "price": 8.99,
                    "category": "Salads",
                    "image": "https://images.unsplash.com/photo-1546793665-c74683f339c1",
                    "available": True,
                    "is_deleted": False
                },
                {
                    "id": "item_004",
                    "name": "Chicken Wings",
                    "description": "Crispy wings with your choice of sauce",
                    "price": 9.99,
                    "category": "Appetizers",
                    "image": "https://images.unsplash.com/photo-1608039829572-78524f79c4c7",
                    "available": True,
                    "is_deleted": False
                },
                {
                    "id": "item_005",
                    "name": "Chocolate Cake",
                    "description": "Rich chocolate cake with ganache",
                    "price": 6.99,
                    "category": "Desserts",
                    "image": "https://images.unsplash.com/photo-1578985545062-69928b1d9587",
                    "available": True,
                    "is_deleted": False
                },
                {
                    "id": "item_006",
                    "name": "Pasta Carbonara",
                    "description": "Creamy pasta with bacon and parmesan",
                    "price": 13.99,
                    "category": "Pasta",
                    "image": "https://images.unsplash.com/photo-1612874742237-6526221588e3",
                    "available": True,
                    "is_deleted": False
                }
            ]
            self._write_json(self.menu_file, default_menu)

        # Initialize orders file
        if not os.path.exists(self.orders_file):
            self._write_json(self.orders_file, [])

        # Initialize restaurant status file
        if not os.path.exists(self.status_file):
            self._write_json(self.status_file, {"is_open": True})

    def _read_json(self, filepath: str):
        with open(filepath, 'r') as f:
            return json.load(f)

    def _write_json(self, filepath: str, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    # User operations
    def get_users(self) -> List[dict]:
        return self._read_json(self.users_file)

    def add_user(self, user: dict):
        users = self.get_users()
        users.append(user)
        self._write_json(self.users_file, users)

    def get_user_by_username(self, username: str) -> Optional[dict]:
        users = self.get_users()
        return next((u for u in users if u['username'] == username), None)

    def get_user_by_email(self, email: str) -> Optional[dict]:
        users = self.get_users()
        return next((u for u in users if u['email'] == email), None)

    # Menu operations
    def get_menu(self) -> List[dict]:
        return self._read_json(self.menu_file)

    def add_menu_item(self, item: dict):
        menu = self.get_menu()
        menu.append(item)
        self._write_json(self.menu_file, menu)

    def update_menu_item(self, item_id: str, updates: dict):
        menu = self.get_menu()
        for item in menu:
            if item['id'] == item_id:
                item.update(updates)
                break
        self._write_json(self.menu_file, menu)
        return next((item for item in menu if item['id'] == item_id), None)

    def toggle_item_availability(self, item_id: str):
        menu = self.get_menu()
        for item in menu:
            if item['id'] == item_id:
                item['available'] = not item['available']
                break
        self._write_json(self.menu_file, menu)

    # Order operations
    def get_orders(self) -> List[dict]:
        return self._read_json(self.orders_file)

    def add_order(self, order: dict):
        orders = self.get_orders()
        orders.append(order)
        self._write_json(self.orders_file, orders)

    def update_order_status(self, order_id: str, status: str):
        orders = self.get_orders()
        for order in orders:
            if order['id'] == order_id:
                order['status'] = status
                break
        self._write_json(self.orders_file, orders)

    # Restaurant status operations
    def get_restaurant_status(self) -> dict:
        return self._read_json(self.status_file)

    def update_restaurant_status(self, is_open: bool):
        self._write_json(self.status_file, {"is_open": is_open})

# Initialize file manager
file_manager = JSONFileManager()

# ============= FASTAPI APP =============

app = FastAPI(title="Delight Cuisine API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============= AUTH ENDPOINTS =============

@app.post("/api/auth/login", response_model=UserResponse)
def login(credentials: LoginRequest):
    # Try to find user by email or username
    user = file_manager.get_user_by_email(credentials.username)
    if not user:
        user = file_manager.get_user_by_username(credentials.username)

    if not user or not pwd_context.verify(credentials.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail="Invalid email/username or password")

    # Verify role matches if requested_role is provided
    if credentials.requested_role:
        if user['role'] != credentials.requested_role:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. This account is not authorized for {credentials.requested_role} access."
            )

    return UserResponse(
        id=user['id'],
        username=user['username'],
        email=user['email'],
        role=user['role'],
        created_at=user['created_at']
    )

@app.post("/api/auth/register", response_model=UserResponse)
def register(user_data: UserCreate):
    # Check if username or email already exists
    existing_username = file_manager.get_user_by_username(user_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_email = file_manager.get_user_by_email(user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = {
        "id": f"user_{datetime.now().timestamp()}",
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": pwd_context.hash(user_data.password),
        "role": user_data.role.value,
        "created_at": datetime.now().isoformat()
    }

    file_manager.add_user(new_user)

    return UserResponse(
        id=new_user['id'],
        username=new_user['username'],
        email=new_user['email'],
        role=new_user['role'],
        created_at=new_user['created_at']
    )

# ============= MENU ENDPOINTS =============

@app.get("/api/menu", response_model=List[MenuItem])
def get_menu():
    return file_manager.get_menu()

@app.post("/api/menu", response_model=MenuItem)
def create_menu_item(item: MenuItem):
    file_manager.add_menu_item(item.dict())
    return item

@app.put("/api/menu/{item_id}", response_model=MenuItem)
def update_menu_item(item_id: str, item: MenuItemUpdate):
    updates = {k: v for k, v in item.dict(exclude_unset=True).items()}
    updated = file_manager.update_menu_item(item_id, updates)

    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found")

    return MenuItem(**updated)

@app.patch("/api/menu/{item_id}/toggle")
def toggle_item_availability(item_id: str):
    file_manager.toggle_item_availability(item_id)
    menu = file_manager.get_menu()
    item = next((i for i in menu if i['id'] == item_id), None)

    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    return {"message": "Item availability toggled", "available": item['available']}

# ============= ORDER ENDPOINTS =============

@app.get("/api/orders", response_model=List[Order])
def get_orders(user_id: Optional[str] = None):
    orders = file_manager.get_orders()
    if user_id:
        orders = [o for o in orders if o['user_id'] == user_id]
    return orders

@app.post("/api/orders", response_model=Order)
def create_order(order: OrderCreate):
    new_order = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "user_id": order.user_id,
        "items": [item.dict() for item in order.items],
        "total": order.total,
        "status": order.status.value,
        "payment_method": order.payment_method.value,
        "order_mode": order.order_mode.value,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    file_manager.add_order(new_order)
    return Order(**new_order)

@app.patch("/api/orders/{order_id}/status")
def update_order_status(order_id: str, status_update: OrderStatusUpdate):
    file_manager.update_order_status(order_id, status_update.status.value)
    return {"message": "Order status updated", "status": status_update.status.value}

# ============= RESTAURANT STATUS =============

@app.get("/api/restaurant/status", response_model=RestaurantStatus)
def get_restaurant_status():
    return file_manager.get_restaurant_status()

@app.put("/api/restaurant/status")
def update_restaurant_status(status_update: RestaurantStatus):
    file_manager.update_restaurant_status(status_update.is_open)
    return {"message": "Restaurant status updated", "is_open": status_update.is_open}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)