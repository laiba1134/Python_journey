# Delight Cuisine - Backend API

Production-ready Flask backend for the Delight Cuisine food ordering system with JWT authentication, RESTful APIs, and clean architecture.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone and navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy .env and update SECRET_KEY and JWT_SECRET_KEY
# Generate secure keys using: python -c "import secrets; print(secrets.token_hex(32))"
```

5. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## 📁 Project Structure

```
backend/
├── app.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── config/
│   └── config.py          # App configuration
├── models/
│   ├── user.py            # User model
│   ├── menu.py            # Menu item model
│   └── order.py           # Order & OrderItem models
├── routes/
│   ├── auth_routes.py     # Authentication endpoints
│   ├── menu_routes.py     # Menu CRUD endpoints
│   └── order_routes.py    # Order management endpoints
├── extensions/
│   ├── db.py              # SQLAlchemy instance
│   └── jwt.py             # JWT configuration
└── utils/
    └── decorators.py      # Custom decorators (admin_required, etc.)
```

## 🔐 Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Default Admin Account
- **Email:** admin@delightcuisine.com
- **Password:** admin123
- **Role:** admin

⚠️ Change this password in production!

## 📡 API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login and get JWT token | No |
| GET | `/me` | Get current user info | Yes |

### Menu Items (`/api/menu`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Get all menu items | No |
| GET | `/<id>` | Get specific menu item | No |
| POST | `/` | Create menu item | Admin |
| PUT | `/<id>` | Update menu item | Admin |
| DELETE | `/<id>` | Delete menu item | Admin |
| GET | `/categories` | Get all categories | No |

### Orders (`/api/orders`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/` | Create new order | Yes |
| GET | `/` | Get user's orders | Yes |
| GET | `/<id>` | Get specific order | Yes |
| GET | `/all` | Get all orders | Admin |
| PATCH | `/<id>/status` | Update order status | Admin |
| DELETE | `/<id>` | Cancel order | Yes |

## 📝 Request/Response Examples

### Register User
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Create Menu Item (Admin)
```bash
POST /api/menu
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "name": "Margherita Pizza",
  "description": "Classic Italian pizza",
  "price": 12.99,
  "category": "main",
  "image_url": "https://example.com/pizza.jpg",
  "available": true
}
```

### Create Order
```bash
POST /api/orders
Authorization: Bearer <user_token>
Content-Type: application/json

{
  "items": [
    {
      "menu_item_id": 1,
      "quantity": 2
    },
    {
      "menu_item_id": 3,
      "quantity": 1
    }
  ],
  "delivery_address": "123 Main St, City",
  "notes": "Extra cheese please"
}
```

### Update Order Status (Admin)
```bash
PATCH /api/orders/1/status
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "status": "preparing"
}
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Flask
FLASK_ENV=development
PORT=5000

# Security (CHANGE IN PRODUCTION)
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production

# Database
DATABASE_URL=sqlite:///delight_cuisine.db

# JWT
JWT_ACCESS_TOKEN_EXPIRES=3600
```

### Database Migration

To switch from SQLite to PostgreSQL:

1. Update `.env`:
```bash
DATABASE_URL=postgresql://user:password@localhost/delight_cuisine
```

2. Install PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

3. Run the app (tables will be created automatically):
```bash
python app.py
```

## 🛡️ Security Features

- ✅ Password hashing using Werkzeug (PBKDF2-SHA256)
- ✅ JWT token-based authentication
- ✅ Role-based access control (admin/customer)
- ✅ Protected admin endpoints
- ✅ CORS configuration
- ✅ Environment variable configuration
- ✅ SQL injection protection via SQLAlchemy ORM

## 🧪 Testing

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Test Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@delightcuisine.com","password":"admin123"}'
```

## 📦 Database Schema

### Users
- id (PK)
- email (unique)
- password (hashed)
- name
- role (admin/customer)
- created_at

### Menu Items
- id (PK)
- name
- description
- price
- category
- image_url
- available
- created_at
- updated_at

### Orders
- id (PK)
- user_id (FK)
- status (pending/preparing/delivered/cancelled)
- total_amount
- delivery_address
- notes
- created_at
- updated_at

### Order Items
- id (PK)
- order_id (FK)
- menu_item_id (FK)
- quantity
- price (at time of order)

## 🚀 Production Deployment

1. **Generate secure keys**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. **Update .env with production values**

3. **Use production database** (PostgreSQL recommended)

4. **Set FLASK_ENV=production**

5. **Use production WSGI server** (gunicorn, uWSGI)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

6. **Enable HTTPS** (use reverse proxy like Nginx)

## 📄 License

MIT License - feel free to use in your projects

## 🤝 Support

For issues or questions, create an issue in the repository.

---

**Built with Flask, SQLAlchemy, and JWT** 🍕