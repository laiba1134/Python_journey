import React, { useState, useEffect } from 'react';
import { User, UserRole, MenuItem, CartItem, Order, OrderStatus, RestaurantStatus, PaymentMethod, OrderMode } from './types';
import { db } from './db';
import Navbar from './components/Navbar';
import MenuPage from './components/MenuPage';
import LoginPage from './components/LoginPage';
import AdminDashboard from './components/AdminDashboard';
import CartPage from './components/CartPage';
import OrdersPage from './components/OrdersPage';

// Helper to check if user is admin (handles both 'admin' and 'ADMIN')
const isAdminUser = (user: User | null): boolean => {
  if (!user) return false;
  return user.role?.toUpperCase() === 'ADMIN';
};

const App: React.FC = () => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [view, setView] = useState<'menu' | 'login' | 'cart' | 'admin' | 'orders'>('menu');
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [restaurantStatus, setRestaurantStatus] = useState<RestaurantStatus>({ isOpen: true });
  const [loading, setLoading] = useState(true);

  // Load initial data from backend
  useEffect(() => {
    const loadData = async () => {
      try {
        // Load menu - include deleted items only if admin
        const menu = await db.getMenu(isAdminUser(currentUser));
        setMenuItems(menu);

        const fetchedOrders = await db.getOrders();
        setOrders(fetchedOrders);

        const status = await db.getRestaurantStatus();
        setRestaurantStatus(status);

        setLoading(false);
      } catch (error) {
        console.error('Failed to load data:', error);
        setLoading(false);
      }
    };

    loadData();
  }, [currentUser?.role]);

  // Handle restaurant status toggle (admin only)
  const handleToggleStatus = async () => {
    const newStatus = {
      isOpen: !restaurantStatus.isOpen,
      message: !restaurantStatus.isOpen
        ? 'We are currently accepting orders!'
        : 'We are currently closed. Please check back later!'
    };

    setRestaurantStatus(newStatus);

    // Only save if user is admin
    if (isAdminUser(currentUser)) {
      try {
        await db.saveRestaurantStatus(newStatus);
        console.log('✅ Restaurant status saved successfully');
      } catch (error) {
        console.error('❌ Failed to save restaurant status:', error);
        // Optionally revert the status on error
        setRestaurantStatus(restaurantStatus);
      }
    }
  };

  const addToCart = (item: MenuItem) => {
    if (!restaurantStatus.isOpen) return;
    setCart(prev => {
      const existing = prev.find(i => i.menuItem.id === item.id);
      if (existing) {
        return prev.map(i => i.menuItem.id === item.id ? { ...i, quantity: i.quantity + 1 } : i);
      }
      return [...prev, { id: Math.random().toString(), menuItem: item, quantity: 1 }];
    });
  };

  const removeFromCart = (id: string) => {
    setCart(prev => prev.filter(i => i.id !== id));
  };

  const placeOrder = async (payment: PaymentMethod, mode: OrderMode) => {
    if (!currentUser) return;
    const newOrder: Order = {
      id: Math.random().toString(36).substr(2, 6).toUpperCase(),
      userId: currentUser.id,
      items: [...cart],
      total: cart.reduce((acc, i) => acc + (i.menuItem.price * i.quantity), 0) + (mode === OrderMode.DELIVERY ? 5 : 0),
      status: OrderStatus.PLACED,
      paymentMethod: payment,
      orderMode: mode,
      timestamp: new Date().toLocaleString(),
    };

    await db.saveOrder(newOrder);
    const fetchedOrders = await db.getOrders();
    setOrders(fetchedOrders);
    setCart([]);
    setView('orders');
  };

  const updateOrderStatus = async (orderId: string, status: OrderStatus) => {
    await db.updateOrderStatus(orderId, status);
    const fetchedOrders = await db.getOrders();
    setOrders(fetchedOrders);
  };

  const handleUpdateMenuItems = async (items: MenuItem[]) => {
    // Batch update all items in the backend
    await db.updateMultipleMenuItems(items);

    // Refresh menu from backend to get the filtered list
    const updatedMenu = await db.getMenu(isAdminUser(currentUser));
    setMenuItems(updatedMenu);
  };

  const toggleAvailability = async (itemId: string) => {
    await db.toggleItemAvailability(itemId);
    const menu = await db.getMenu(isAdminUser(currentUser));
    setMenuItems(menu);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0a0a0a]">
        <div className="text-amber-500 text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-[#0a0a0a]">
      <Navbar
        user={currentUser}
        onNavigate={setView}
        onLogout={() => { setCurrentUser(null); setView('menu'); }}
        cartCount={cart.reduce((a, b) => a + b.quantity, 0)}
      />

      <main className="flex-grow pt-24 container mx-auto px-4 pb-12">
        {!restaurantStatus.isOpen && view !== 'admin' && (
          <div className="bg-amber-900/20 border border-amber-500/50 text-amber-500 p-4 rounded-2xl mb-8 text-center text-[10px] font-black tracking-[0.2em] animate-pulse uppercase">
            ⚠️ Restricted: Cuisine Offline. Browsing Mode Only.
          </div>
        )}

        {view === 'menu' && (
          <MenuPage
            items={menuItems}
            onAddToCart={addToCart}
            isClosed={!restaurantStatus.isOpen}
            isLoggedIn={!!currentUser}
            onPromptLogin={() => setView('login')}
          />
        )}

        {view === 'login' && (
          <LoginPage onLogin={async (usernameOrEmail, password) => {
            const user = await db.login(usernameOrEmail, password);

            if (user) {
              setCurrentUser(user);
              setView(isAdminUser(user) ? 'admin' : 'menu');
            } else {
              alert('Invalid credentials or access denied.');
            }
          }} />
        )}

        {view === 'cart' && (
          <CartPage cart={cart} onRemove={removeFromCart} onCheckout={placeOrder} isClosed={!restaurantStatus.isOpen} />
        )}

        {view === 'orders' && (
          <OrdersPage orders={isAdminUser(currentUser) ? orders : orders.filter(o => o.userId === currentUser?.id)} />
        )}

        {view === 'admin' && (
          <>
            {isAdminUser(currentUser) ? (
              <AdminDashboard
                items={menuItems}
                orders={orders}
                restaurantStatus={restaurantStatus}
                onToggleStatus={handleToggleStatus}
                onUpdateOrder={updateOrderStatus}
                onToggleItem={toggleAvailability}
                onUpdateMenuItems={handleUpdateMenuItems}
              />
            ) : (
              <div className="text-center py-16">
                <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-6 rounded-2xl inline-block">
                  <h3 className="text-2xl font-black mb-2">ACCESS DENIED</h3>
                  <p className="text-sm">You do not have permission to access the admin dashboard.</p>
                  <button
                    onClick={() => setView('menu')}
                    className="mt-4 honey-gradient text-black px-6 py-2 rounded-xl font-black text-xs"
                  >
                    RETURN TO MENU
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </main>

      <footer className="bg-black border-t border-white/10 pt-16 pb-8">
        <div className="container mx-auto px-6 text-center md:text-left">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">
            <div className="space-y-6">
              <div className="flex items-center gap-2 justify-center md:justify-start">
                <div className="w-8 h-8 honey-gradient rounded-lg flex items-center justify-center font-bold text-black shadow-lg shadow-amber-500/20">D</div>
                <span className="text-2xl font-black tracking-tight honey-text">DELIGHT<span className="text-white">CUISINE</span></span>
              </div>
              <p className="text-white/40 text-sm leading-relaxed">
                Elevating the art of dining with premium artisanal flavors delivered straight to your doorstep.
              </p>
              <div className="flex items-center gap-4 justify-center md:justify-start pt-2">
                <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-white/40 hover:text-amber-500 hover:border-amber-500/50 hover:bg-amber-500/5 transition-all">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" /></svg>
                </a>
                <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-white/40 hover:text-amber-500 hover:border-amber-500/50 hover:bg-amber-500/5 transition-all">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.041-1.416-4.041-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" /></svg>
                </a>
                <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-white/40 hover:text-amber-500 hover:border-amber-500/50 hover:bg-amber-500/5 transition-all">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.84 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z" /></svg>
                </a>
              </div>
            </div>
            <div>
              <h4 className="text-white font-bold mb-6 text-sm uppercase tracking-widest">Navigation</h4>
              <ul className="space-y-4 text-sm text-white/40 font-medium">
                <li><button onClick={() => setView('menu')} className="hover:honey-text transition-colors">Browse Menu</button></li>
                <li><button onClick={() => setView('orders')} className="hover:honey-text transition-colors">Order Tracking</button></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-bold mb-6 text-sm uppercase tracking-widest">Support</h4>
              <ul className="space-y-4 text-sm text-white/40 font-medium">
                <li><a href="#" className="hover:honey-text transition-colors">Help Center</a></li>
                <li><a href="#" className="hover:honey-text transition-colors">Safety Guidelines</a></li>
              </ul>
            </div>
            <div className="space-y-6">
              <h4 className="text-white font-bold text-sm uppercase tracking-widest">Stay Updated</h4>
              <div className="flex flex-col gap-2">
                <input
                  type="email"
                  placeholder="Email address"
                  className="bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm outline-none focus:border-amber-500 transition-all"
                />
                <button className="honey-gradient text-black font-black text-xs py-3.5 rounded-xl uppercase tracking-widest">Subscribe</button>
              </div>
            </div>
          </div>
          <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 text-white/20 text-[10px] font-bold uppercase tracking-widest">
            <p>&copy; 2024 Delight Cuisine Inc.</p>
            <span className="honey-text">#DelightCuisine</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;