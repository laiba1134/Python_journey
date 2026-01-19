
import React, { useState, useMemo } from 'react';
import { MenuItem } from '../types';

interface MenuPageProps {
  items: MenuItem[];
  onAddToCart: (item: MenuItem) => void;
  isClosed: boolean;
  isLoggedIn: boolean;
  onPromptLogin: () => void;
}

const MenuPage: React.FC<MenuPageProps> = ({ items, onAddToCart, isClosed, isLoggedIn, onPromptLogin }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const categories = useMemo(() => {
    return ['All', ...Array.from(new Set(items.map(i => i.category)))];
  }, [items]);

  const filteredItems = useMemo(() => {
    return items.filter(item => {
      const matchesSearch = item.name.toLowerCase().includes(searchQuery.toLowerCase()) || 
                            item.category.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCategory = selectedCategory === 'All' || item.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });
  }, [items, searchQuery, selectedCategory]);

  return (
    <div className="space-y-12">
      {/* HERO SECTION WITH GREY FOOD BACKGROUND */}
      <div className="relative rounded-[2.5rem] overflow-hidden min-h-[450px] flex items-center justify-center border border-white/10 shadow-2xl">
        {/* Background Layer */}
        <div className="absolute inset-0 z-0">
          <img 
            src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1600&q=80" 
            alt="Delicious food background"
            className="w-full h-full object-cover grayscale opacity-30 contrast-125 brightness-50 scale-105"
          />
          {/* Gradient Overlay for Readability */}
          <div className="absolute inset-0 bg-gradient-to-b from-black/80 via-black/40 to-[#0a0a0a]"></div>
        </div>

        {/* Hero Content Layer */}
        <header className="relative z-10 w-full max-w-4xl px-6 py-16 text-center space-y-8">
          <div className="space-y-4">
            <h1 className="text-5xl md:text-7xl font-black tracking-tighter leading-none animate-in fade-in slide-in-from-bottom-4 duration-700">
              DELIGHT <span className="honey-text">CUISINE</span>
            </h1>
            <p className="text-white/70 max-w-xl mx-auto text-lg md:text-xl font-medium tracking-wide">
              The golden standard of artisanal gastronomy, delivered with precision.
            </p>
          </div>

          {/* Search Bar - Glassmorphism style */}
          <div className="relative group max-w-2xl mx-auto">
            <div className="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
              <svg className="h-6 w-6 text-amber-500/50 group-focus-within:text-amber-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input 
              type="text"
              placeholder="Search our gourmet selection..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-black/60 backdrop-blur-xl border border-white/10 rounded-2xl py-5 pl-14 pr-6 outline-none focus:border-amber-500 focus:ring-2 focus:ring-amber-500/20 transition-all text-lg shadow-2xl placeholder:text-white/20"
            />
          </div>

          {/* Categories Bar */}
          <div className="flex flex-wrap justify-center gap-3 pt-4">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-8 py-3 rounded-xl text-xs font-black tracking-widest transition-all border uppercase ${
                  selectedCategory === cat 
                  ? 'honey-gradient text-black border-amber-400 shadow-[0_0_20px_rgba(245,158,11,0.3)]' 
                  : 'bg-white/5 backdrop-blur-md text-white/50 border-white/10 hover:border-white/30 hover:text-white'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </header>
      </div>

      {/* Menu Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        {filteredItems.length > 0 ? (
          filteredItems.map(item => (
            <div key={item.id} className="glass-panel rounded-[2rem] overflow-hidden group hover:border-amber-500/50 transition-all duration-500 flex flex-col hover:shadow-[0_20px_50px_rgba(0,0,0,0.5)]">
              <div className="relative h-64 w-full overflow-hidden bg-white/5">
                <img 
                  src={item.image_url} 
                  alt={item.name} 
                  loading="eager"
                  className="w-full h-full object-cover transition-transform duration-1000 group-hover:scale-110"
                  onError={(e) => {
                    e.currentTarget.src = "https://images.unsplash.com/photo-1495195129352-aec325a55b65?auto=format&fit=crop&w=800&q=80";
                  }}
                />
                <div className="absolute top-5 right-5 px-4 py-1.5 bg-black/80 backdrop-blur-md rounded-full text-[10px] font-black honey-text border border-amber-500/30 uppercase tracking-widest">
                  {item.category}
                </div>
                {!item.is_available && (
                  <div className="absolute inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center font-black text-red-500 tracking-tighter text-2xl rotate-[-5deg] border-2 border-red-500/50 m-4 rounded-xl">
                    SOLD OUT
                  </div>
                )}
              </div>
              <div className="p-7 space-y-5 flex-grow flex flex-col">
                <div className="flex justify-between items-start gap-4">
                  <h3 className="font-black text-xl leading-tight group-hover:honey-text transition-colors duration-300">{item.name}</h3>
                  <span className="honey-text font-black text-2xl tracking-tighter">${item.price.toFixed(2)}</span>
                </div>
                <p className="text-white/40 text-sm leading-relaxed flex-grow font-medium italic">"{item.description}"</p>
                
                <div className="pt-2">
                  {isClosed ? (
                    <div className="w-full py-4 rounded-xl bg-white/5 text-white/20 text-center text-xs font-black uppercase tracking-widest border border-white/5">
                      Kitchen Closed
                    </div>
                  ) : !isLoggedIn ? (
                    <button 
                      onClick={onPromptLogin}
                      className="w-full py-4 rounded-xl border-2 border-amber-500/30 text-amber-500 hover:bg-amber-500 hover:text-black transition-all text-xs font-black uppercase tracking-widest"
                    >
                      Login to Order
                    </button>
                  ) : item.is_available ? (
                    <button 
                      onClick={() => onAddToCart(item)}
                      className="w-full py-4 rounded-xl bg-amber-500 text-black hover:bg-amber-400 transition-all text-xs font-black shadow-xl shadow-amber-500/20 active:scale-95 uppercase tracking-widest"
                    >
                      Add to Basket
                    </button>
                  ) : (
                    <div className="w-full py-4 rounded-xl bg-white/5 text-white/20 text-center text-xs font-black uppercase tracking-widest">
                      Out of Stock
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full py-32 text-center space-y-6 glass-panel rounded-[3rem]">
            <div className="text-8xl opacity-20">🍽️</div>
            <h3 className="text-3xl font-black tracking-tight">Mmm, nothing found...</h3>
            <p className="text-white/30 max-w-sm mx-auto">Our chefs are talented, but they haven't invented that dish yet. Try another search!</p>
            <button 
              onClick={() => { setSearchQuery(''); setSelectedCategory('All'); }}
              className="honey-text font-black text-sm tracking-widest uppercase hover:underline underline-offset-8"
            >
              Reset Filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default MenuPage;
