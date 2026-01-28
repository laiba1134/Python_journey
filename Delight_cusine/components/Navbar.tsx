import React from 'react';
import { User, UserRole } from '../types';

interface NavbarProps {
  user: User | null;
  onNavigate: (view: 'menu' | 'login' | 'cart' | 'admin' | 'orders') => void;
  onLogout: () => void;
  cartCount: number;
}

const Navbar: React.FC<NavbarProps> = ({ user, onNavigate, onLogout, cartCount }) => {
  // Normalize role comparison - handles both 'admin' and 'ADMIN'
  const isAdmin = user?.role?.toUpperCase() === 'ADMIN';

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass-panel border-b border-white/10 h-16 flex items-center px-6">
      <div className="container mx-auto flex justify-between items-center">
        <div
          className="flex items-center gap-2 cursor-pointer"
          onClick={() => onNavigate('menu')}
        >
          <div className="w-8 h-8 honey-gradient rounded-lg flex items-center justify-center font-bold text-black shadow-lg shadow-amber-500/20">D</div>
          <span className="text-xl font-bold tracking-tight honey-text">DELIGHT<span className="text-white">CUISINE</span></span>
        </div>

        <div className="flex items-center gap-6">
          <button onClick={() => onNavigate('menu')} className="text-white/70 hover:text-amber-400 transition-colors text-sm font-medium">Menu</button>

          {user ? (
            <>
              {isAdmin ? (
                <button onClick={() => onNavigate('admin')} className="text-white/70 hover:text-amber-400 transition-colors text-sm font-medium">Dashboard</button>
              ) : (
                <>
                  <button onClick={() => onNavigate('orders')} className="text-white/70 hover:text-amber-400 transition-colors text-sm font-medium">My Orders</button>
                  <button
                    onClick={() => onNavigate('cart')}
                    className="relative flex items-center gap-2 text-white/70 hover:text-amber-400 transition-colors text-sm font-medium"
                  >
                    Cart
                    {cartCount > 0 && (
                      <span className="absolute -top-2 -right-3 px-1.5 py-0.5 honey-gradient text-black text-[10px] font-bold rounded-full">{cartCount}</span>
                    )}
                  </button>
                </>
              )}
              <button onClick={onLogout} className="bg-white/5 hover:bg-white/10 border border-white/10 px-4 py-1.5 rounded-lg text-sm transition-all">Logout</button>
            </>
          ) : (
            <button
              onClick={() => onNavigate('login')}
              className="honey-gradient hover:opacity-90 text-black px-5 py-2 rounded-lg text-sm font-bold transition-all shadow-md shadow-amber-500/10"
            >
              Login / Register
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;