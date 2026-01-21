import React from 'react';
import { MenuItem } from '../types';

interface MenuPageProps {
  items: MenuItem[];
  onAddToCart: (item: MenuItem) => void;
  isClosed: boolean;
  isLoggedIn: boolean;
  onPromptLogin: () => void;
}

const MenuPage: React.FC<MenuPageProps> = ({ items, onAddToCart, isClosed, isLoggedIn, onPromptLogin }) => {
  const categories = Array.from(new Set(items.map(item => item.category)));

  const handleAddToCart = (item: MenuItem) => {
    if (!isLoggedIn) {
      onPromptLogin();
      return;
    }
    if (isClosed || !item.available) {
      return;
    }
    onAddToCart(item);
  };

  // Check if item is unavailable (either restaurant closed OR item marked unavailable)
  const isItemUnavailable = (item: MenuItem) => {
    return isClosed || !item.available;
  };

  return (
    <div className="space-y-16">
      <div className="text-center space-y-4">
        <h1 className="text-6xl md:text-7xl font-black tracking-tighter honey-text">
          MENU
        </h1>
        <p className="text-white/40 text-lg max-w-2xl mx-auto">
          Discover our carefully curated selection of artisanal dishes
        </p>
      </div>

      {categories.map(category => (
        <div key={category} className="space-y-8">
          <h2 className="text-3xl font-black tracking-tight honey-text border-b border-white/10 pb-4">
            {category}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {items.filter(item => item.category === category).map(item => {
              const unavailable = isItemUnavailable(item);

              return (
                <div
                  key={item.id}
                  className={`glass-panel rounded-3xl overflow-hidden border border-white/10 transition-all ${unavailable
                      ? 'opacity-60 cursor-not-allowed'
                      : 'hover:scale-[1.02] hover:shadow-2xl hover:shadow-amber-500/10'
                    }`}
                >
                  <div className="relative h-48 overflow-hidden">
                    <img
                      src={item.image}
                      alt={item.name}
                      className={`w-full h-full object-cover ${unavailable ? 'grayscale' : ''}`}
                    />
                    {unavailable && (
                      <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
                        <div className="bg-red-500/20 border border-red-500 text-red-500 px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest">
                          {isClosed ? '🔒 Restaurant Closed' : '❌ Sold Out'}
                        </div>
                      </div>
                    )}
                    {!unavailable && (
                      <div className="absolute top-4 right-4">
                        <div className="honey-gradient px-3 py-1.5 rounded-full text-black text-xs font-black shadow-lg">
                          ${item.price.toFixed(2)}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="p-6 space-y-4">
                    <div>
                      <h3 className="text-xl font-black text-white mb-2">{item.name}</h3>
                      <p className="text-white/40 text-sm leading-relaxed">{item.description}</p>
                    </div>

                    <div className="flex items-center justify-between pt-2">
                      {unavailable && (
                        <div className="text-2xl font-black text-white/20">
                          ${item.price.toFixed(2)}
                        </div>
                      )}

                      <button
                        onClick={() => handleAddToCart(item)}
                        disabled={unavailable}
                        className={`${unavailable
                            ? 'bg-white/5 text-white/20 cursor-not-allowed'
                            : 'honey-gradient text-black hover:scale-105 active:scale-95 shadow-lg shadow-amber-500/20'
                          } px-6 py-3 rounded-xl font-black text-sm transition-all uppercase tracking-wider ${!unavailable ? 'ml-auto' : 'w-full'}`}
                      >
                        {unavailable
                          ? (isClosed ? 'Closed' : 'Unavailable')
                          : 'Add to Cart'
                        }
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
};

export default MenuPage;