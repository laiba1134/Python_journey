import React, { useState } from 'react';
import { MenuItem } from '../types';

interface MenuPageProps {
  items: MenuItem[];
  onAddToCart: (item: MenuItem) => void;
  isClosed: boolean;
  isLoggedIn: boolean;
  onPromptLogin: () => void;
}

const MenuPage: React.FC<MenuPageProps> = ({ items, onAddToCart, isClosed, isLoggedIn, onPromptLogin }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');

  // Extract unique categories and capitalize them properly
  const uniqueCategories = Array.from(new Set(items.map(item => item.category?.toLowerCase() || 'other')));
  const categories = ['ALL', ...uniqueCategories.map(cat => cat.toUpperCase())];

  console.log('Available categories:', categories); // Debug log

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

  // Filter items based on search and category
  const filteredItems = items.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'ALL' ||
      item.category?.toLowerCase() === selectedCategory.toLowerCase();
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-8 py-12">
        <h1 className="text-6xl md:text-8xl font-black tracking-tighter">
          <span className="text-white">DELIGHT </span>
          <span className="honey-text">CUISINE</span>
        </h1>
        <p className="text-white/60 text-lg md:text-xl max-w-3xl mx-auto leading-relaxed">
          The golden standard of artisanal gastronomy, delivered with precision.
        </p>

        {/* Search Bar */}
        <div className="max-w-2xl mx-auto">
          <input
            type="text"
            placeholder="Search our gourmet selection..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-white/5 border border-white/10 rounded-2xl px-8 py-5 text-white placeholder:text-white/30 outline-none focus:border-amber-500 transition-all text-lg"
          />
        </div>

        {/* Category Filters */}
        <div className="flex flex-wrap justify-center gap-3 pt-4">
          {categories.map(category => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-6 py-3 rounded-xl font-black text-xs uppercase tracking-widest transition-all ${selectedCategory === category
                  ? 'honey-gradient text-black shadow-lg'
                  : 'bg-white/5 text-white/40 hover:text-white hover:bg-white/10 border border-white/10'
                }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Category Stats */}
        <div className="text-white/40 text-sm">
          Showing {filteredItems.length} of {items.length} items
        </div>
      </div>

      {/* Menu Items Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {filteredItems.map(item => {
          const unavailable = isItemUnavailable(item);

          return (
            <div
              key={item.id}
              className={`glass-panel rounded-3xl overflow-hidden border border-white/10 transition-all ${unavailable
                  ? 'opacity-60 cursor-not-allowed'
                  : 'hover:scale-[1.02] hover:shadow-2xl hover:shadow-amber-500/10'
                }`}
            >
              {/* Item Image */}
              <div className="relative h-56 overflow-hidden">
                <img
                  src={item.image}
                  alt={item.name}
                  className={`w-full h-full object-cover ${unavailable ? 'grayscale' : ''}`}
                  onError={(e) => {
                    // Fallback image if image fails to load
                    e.currentTarget.src = 'https://via.placeholder.com/400x300/0a0a0a/fbbf24?text=' + encodeURIComponent(item.name);
                  }}
                />

                {/* Category Badge */}
                <div className="absolute top-4 left-4">
                  <div className="bg-black/60 backdrop-blur-sm px-3 py-1.5 rounded-full text-amber-500 text-[10px] font-black uppercase tracking-widest border border-amber-500/30">
                    {item.category}
                  </div>
                </div>

                {/* Unavailable Overlay */}
                {unavailable && (
                  <div className="absolute inset-0 bg-black/70 flex items-center justify-center">
                    <div className="bg-red-500/20 border border-red-500 text-red-500 px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest">
                      {isClosed ? '🔒 Restaurant Closed' : '❌ Sold Out'}
                    </div>
                  </div>
                )}
              </div>

              {/* Item Details */}
              <div className="p-5 space-y-4">
                <div>
                  <h3 className="text-xl font-black text-white mb-1">{item.name}</h3>
                  <p className="text-white/40 text-sm leading-relaxed italic">"{item.description}"</p>
                </div>

                {/* Price and Add Button */}
                <div className="flex items-center justify-between pt-2">
                  <div className={`text-2xl font-black ${unavailable ? 'text-white/20' : 'honey-text'}`}>
                    ${item.price.toFixed(2)}
                  </div>
                </div>

                <button
                  onClick={() => handleAddToCart(item)}
                  disabled={unavailable}
                  className={`w-full py-3 rounded-xl font-black text-sm uppercase tracking-wider transition-all ${unavailable
                      ? 'bg-white/5 text-white/20 cursor-not-allowed border border-white/5'
                      : 'honey-gradient text-black hover:scale-105 active:scale-95 shadow-lg shadow-amber-500/20 border border-amber-500/50'
                    }`}
                >
                  {unavailable
                    ? (isClosed ? 'Closed' : 'Unavailable')
                    : isLoggedIn ? 'Add to Cart' : 'Login to Order'
                  }
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* No Results */}
      {filteredItems.length === 0 && (
        <div className="text-center py-16">
          <p className="text-white/40 text-lg">No items found matching your search.</p>
        </div>
      )}
    </div>
  );
};

export default MenuPage;