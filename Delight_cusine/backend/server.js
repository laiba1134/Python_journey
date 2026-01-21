import express from 'express';
import cors from 'cors';
import Database from 'better-sqlite3';

const app = express();
const db = new Database('delight-cuisine.db');

app.use(cors());
app.use(express.json());

// Initialize database tables
db.exec(`
  CREATE TABLE IF NOT EXISTS menu_items (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    is_available INTEGER DEFAULT 1,
    is_deleted INTEGER DEFAULT 0,
    image_url TEXT
  );

  CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    name TEXT NOT NULL
  );

  CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    userId TEXT NOT NULL,
    items TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT NOT NULL,
    paymentMethod TEXT NOT NULL,
    orderMode TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (userId) REFERENCES users(id)
  );
`);

// Seed initial menu if empty
const menuCount = db.prepare('SELECT COUNT(*) as count FROM menu_items').get();
if (menuCount.count === 0) {
  const initialMenu = [
    { id: '1', name: 'Delight Truffle Burger', description: 'Double beef patty, truffle mayo, and a drizzle of spicy honey.', price: 18.50, category: 'Burgers', is_available: 1, image_url: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80' },
    { id: '2', name: 'Golden Glazed Wings', description: 'Crispy wings tossed in a signature honey-soy glaze.', price: 12.00, category: 'Appetizers', is_available: 1, image_url: 'https://images.unsplash.com/photo-1567620832903-9fc6debc209f?auto=format&fit=crop&w=800&q=80' },
    { id: '3', name: 'Seasonal Root Salad', description: 'Seasonal vegetables, goat cheese, and honey balsamic vinaigrette.', price: 14.50, category: 'Salads', is_available: 1, image_url: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80' },
    { id: '4', name: 'Spicy Delight Pizza', description: 'Hot salami, mozzarella, and a generous honey swirl.', price: 21.00, category: 'Main Courses', is_available: 1, image_url: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80' },
    { id: '5', name: 'Artisan Charcuterie', description: 'Premium cured meats, honeycomb, and aged cheeses.', price: 24.00, category: 'Appetizers', is_available: 1, image_url: 'https://images.unsplash.com/photo-1559183030-89d9333bb3c5?auto=format&fit=crop&w=800&q=80' },
    { id: '6', name: 'Wildflower Pasta', description: 'Handmade pappardelle with butter, sage, and honey-parmesan tuile.', price: 19.50, category: 'Main Courses', is_available: 1, image_url: 'https://images.unsplash.com/photo-1473093226795-af9932fe5855?auto=format&fit=crop&w=800&q=80' },
    { id: '7', name: 'Smoked Salmon Toast', description: 'Sourdough, cream cheese, capers, and a hint of citrus honey.', price: 16.00, category: 'Breakfast', is_available: 1, image_url: 'https://images.unsplash.com/photo-1484723088339-17e83d908c51?auto=format&fit=crop&w=800&q=80' },
    { id: '8', name: 'Lavender Cheesecake', description: 'Velvety cheesecake infused with local lavender and honey.', price: 9.50, category: 'Desserts', is_available: 1, image_url: 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=800&q=80' },
  ];

  const insertMenu = db.prepare('INSERT INTO menu_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
  initialMenu.forEach(item => {
    insertMenu.run(item.id, item.name, item.description, item.price, item.category, item.is_available, 0, item.image_url);
  });
}

// Seed default users if empty
const userCount = db.prepare('SELECT COUNT(*) as count FROM users').get();
if (userCount.count === 0) {
  const insertUser = db.prepare('INSERT INTO users VALUES (?, ?, ?, ?, ?)');
  insertUser.run('1', 'admin', 'admin123', 'admin', 'Admin User');
  insertUser.run('2', 'customer', 'customer123', 'customer', 'Customer User');
}

// API Routes

// Get all menu items
app.get('/api/menu', (req, res) => {
  const items = db.prepare('SELECT * FROM menu_items WHERE is_deleted = 0').all();
  res.json(items.map(item => ({
    ...item,
    is_available: Boolean(item.is_available),
    is_deleted: Boolean(item.is_deleted)
  })));
});

// Add new menu item
app.post('/api/menu', (req, res) => {
  const { id, name, description, price, category, is_available, image_url } = req.body;
  try {
    const insert = db.prepare('INSERT INTO menu_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
    insert.run(id, name, description, price, category, is_available ? 1 : 0, 0, image_url);
    res.json({ success: true });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Update menu item
app.put('/api/menu/:id', (req, res) => {
  const { name, description, price, category, is_available, is_deleted, image_url } = req.body;
  const update = db.prepare(`
    UPDATE menu_items
    SET name = ?, description = ?, price = ?, category = ?, is_available = ?, is_deleted = ?, image_url = ?
    WHERE id = ?
  `);
  update.run(name, description, price, category, is_available ? 1 : 0, is_deleted ? 1 : 0, image_url, req.params.id);
  res.json({ success: true });
});

// Delete menu item (soft delete)
app.delete('/api/menu/:id', (req, res) => {
  const update = db.prepare('UPDATE menu_items SET is_deleted = 1 WHERE id = ?');
  update.run(req.params.id);
  res.json({ success: true });
});

// Toggle availability
app.patch('/api/menu/:id/availability', (req, res) => {
  const item = db.prepare('SELECT is_available FROM menu_items WHERE id = ?').get(req.params.id);
  const update = db.prepare('UPDATE menu_items SET is_available = ? WHERE id = ?');
  update.run(item.is_available ? 0 : 1, req.params.id);
  res.json({ success: true });
});

// User login
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;
  const user = db.prepare('SELECT * FROM users WHERE username = ? AND password = ?').get(username, password);
  if (user) {
    res.json(user);
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

// Get all orders
app.get('/api/orders', (req, res) => {
  const orders = db.prepare('SELECT * FROM orders').all();
  res.json(orders.map(order => ({
    ...order,
    items: JSON.parse(order.items)
  })));
});

// Get orders by user
app.get('/api/orders/user/:userId', (req, res) => {
  const orders = db.prepare('SELECT * FROM orders WHERE userId = ?').all(req.params.userId);
  res.json(orders.map(order => ({
    ...order,
    items: JSON.parse(order.items)
  })));
});

// Create order
app.post('/api/orders', (req, res) => {
  const { id, userId, items, total, status, paymentMethod, orderMode, timestamp } = req.body;
  const insert = db.prepare('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)');
  insert.run(id, userId, JSON.stringify(items), total, status, paymentMethod, orderMode, timestamp);
  res.json({ success: true, orderId: id });
});

// Update order status
app.patch('/api/orders/:id/status', (req, res) => {
  const { status } = req.body;
  const update = db.prepare('UPDATE orders SET status = ? WHERE id = ?');
  update.run(status, req.params.id);
  res.json({ success: true });
});

// Restaurant status (using a simple in-memory store for now)
let restaurantStatus = { isOpen: true };

app.get('/api/restaurant/status', (req, res) => {
  res.json(restaurantStatus);
});

app.post('/api/restaurant/status', (req, res) => {
  restaurantStatus = req.body;
  res.json({ success: true });
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`🚀 Backend server running on http://localhost:${PORT}`);
});