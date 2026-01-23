import React, { useState } from 'react';
import { MenuItem, Order, OrderStatus, RestaurantStatus } from '../types';

interface AdminDashboardProps {
  items: MenuItem[];
  orders: Order[];
  restaurantStatus: RestaurantStatus;
  onToggleStatus: () => void;
  onUpdateOrder: (id: string, status: OrderStatus) => void;
  onToggleItem: (id: string) => void;
  onUpdateMenuItems: (items: MenuItem[]) => void;
}

const AdminDashboard: React.FC<AdminDashboardProps> = ({
  items, orders, restaurantStatus, onToggleStatus, onUpdateOrder, onToggleItem, onUpdateMenuItems
}) => {
  const [activeTab, setActiveTab] = useState<'orders' | 'menu'>('orders');
  const [editingItem, setEditingItem] = useState<MenuItem | null>(null);
  const [isFormOpen, setIsFormOpen] = useState(false);

  // Filter out items already marked as deleted for the admin view
  const visibleItems = items.filter(i => !i.is_deleted);

  // Form State
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    category: '',
    image: ''
  });

  const openAddForm = () => {
    setEditingItem(null);
    setFormData({ name: '', description: '', price: '', category: '', image: '' });
    setIsFormOpen(true);
  };

  const openEditForm = (item: MenuItem) => {
    setEditingItem(item);
    setFormData({
      name: item.name,
      description: item.description,
      price: item.price.toString(),
      category: item.category,
      image: item.image
    });
    setIsFormOpen(true);
  };

  const handleDelete = (id: string) => {
    const confirmed = window.confirm('REMOVAL PROTOCOL: Confirm permanent removal of this item from the active inventory?');

    if (confirmed) {
      // Soft-delete implementation: mark the item as deleted in the master list
      const updatedList = items.map(item =>
        item.id === id ? { ...item, is_deleted: true } : item
      );

      onUpdateMenuItems(updatedList);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const priceValue = parseFloat(formData.price);

    if (isNaN(priceValue)) {
      alert("Invalid price format.");
      return;
    }

    const newItem: MenuItem = {
      id: editingItem ? editingItem.id : Math.random().toString(36).substr(2, 9),
      name: formData.name,
      description: formData.description,
      price: priceValue,
      category: formData.category,
      image: formData.image || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500',
      available: editingItem ? editingItem.available : true,
      is_deleted: false
    };

    let updatedMenu: MenuItem[];
    if (editingItem) {
      updatedMenu = items.map(i => i.id === editingItem.id ? newItem : i);
    } else {
      updatedMenu = [...items, newItem];
    }

    onUpdateMenuItems(updatedMenu);
    setIsFormOpen(false);
    setEditingItem(null);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h1 className="text-3xl font-black tracking-tighter honey-text uppercase">System Command</h1>
          <p className="text-white/40 font-medium text-sm">Inventory & logistics management.</p>
        </div>

        <div className="glass-panel p-4 rounded-2xl flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${restaurantStatus.isOpen ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
            <span className="font-black text-[10px] tracking-widest uppercase">{restaurantStatus.isOpen ? 'LIVE' : 'OFFLINE'}</span>
          </div>
          <button
            onClick={onToggleStatus}
            className={`px-6 py-2 rounded-xl text-[10px] font-black transition-all uppercase tracking-widest border ${restaurantStatus.isOpen ? 'bg-red-500/10 text-red-500 border-red-500/30 hover:bg-red-500/20' : 'bg-green-500/20 text-green-500 border-green-500/30 hover:bg-green-500/30'}`}
          >
            {restaurantStatus.isOpen ? 'Close Shop' : 'Initialize Cuisine'}
          </button>
        </div>
      </div>

      <div className="flex border-b border-white/5 gap-8">
        <button
          onClick={() => { setActiveTab('orders'); setIsFormOpen(false); }}
          className={`pb-4 text-[10px] font-black tracking-[0.2em] transition-all uppercase ${activeTab === 'orders' ? 'border-b-2 honey-border honey-text' : 'text-white/30'}`}
        >
          Orders Queue ({orders.length})
        </button>
        <button
          onClick={() => { setActiveTab('menu'); setIsFormOpen(false); }}
          className={`pb-4 text-[10px] font-black tracking-[0.2em] transition-all uppercase ${activeTab === 'menu' ? 'border-b-2 honey-border honey-text' : 'text-white/30'}`}
        >
          Inventory Manager ({visibleItems.length})
        </button>
      </div>

      {activeTab === 'orders' && !isFormOpen && (
        <div className="grid gap-4">
          {orders.length === 0 ? (
            <div className="glass-panel p-20 text-center text-white/10 font-black italic rounded-[2rem] border-dashed border-2 uppercase tracking-widest">
              No active transmissions
            </div>
          ) : (
            orders.map(order => (
              <div key={order.id} className="glass-panel p-6 rounded-[2rem] flex flex-col md:flex-row justify-between gap-6 border border-white/5">
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <span className="font-mono font-black honey-text text-lg">#{order.id}</span>
                    <span className="text-[10px] bg-white/5 px-3 py-1 rounded-full text-white/40 font-bold uppercase tracking-widest">{order.timestamp}</span>
                  </div>
                  <div className="space-y-1">
                    {order.items.map((i, idx) => (
                      <p key={idx} className="text-sm font-medium text-white/80">
                        • {i.menuItem.name} <span className="text-amber-500/50">x{i.quantity}</span>
                      </p>
                    ))}
                  </div>
                  <p className="font-black text-xl tracking-tighter">${order.total.toFixed(2)}</p>
                </div>

                <div className="flex flex-wrap items-center gap-2 content-center">
                  {Object.values(OrderStatus).map(status => (
                    <button
                      key={status}
                      onClick={() => onUpdateOrder(order.id, status)}
                      className={`px-4 py-2 rounded-xl text-[9px] font-black tracking-widest transition-all uppercase border ${order.status === status ? 'bg-amber-500 text-black border-amber-500 shadow-lg shadow-amber-500/20' : 'bg-white/5 text-white/40 border-white/5 hover:border-white/20'}`}
                    >
                      {status}
                    </button>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'menu' && (
        <div className="space-y-6">
          {!isFormOpen ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <button
                onClick={openAddForm}
                className="glass-panel p-6 rounded-[2rem] border-2 border-dashed border-white/10 flex flex-col items-center justify-center gap-4 text-white/20 hover:text-amber-500 hover:border-amber-500/50 transition-all group min-h-[180px]"
              >
                <div className="w-12 h-12 rounded-full border-2 border-current flex items-center justify-center group-hover:scale-110 transition-transform">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 4v16m8-8H4"></path></svg>
                </div>
                <span className="text-xs font-black uppercase tracking-[0.2em]">Add New Item</span>
              </button>

              {visibleItems.map(item => (
                <div key={item.id} className="glass-panel p-5 rounded-[2rem] flex flex-col border border-white/5 hover:border-white/20 transition-all group">
                  <div className="flex items-center gap-4 mb-4">
                    <img src={item.image} className="w-20 h-20 object-cover rounded-2xl shadow-2xl" alt={item.name} />
                    <div className="flex-grow">
                      <h4 className="font-black text-sm uppercase tracking-tight truncate group-hover:honey-text transition-colors">{item.name}</h4>
                      <p className="text-[9px] text-white/30 font-black tracking-widest uppercase">{item.category}</p>
                      <p className="honey-text font-black text-lg mt-1 tracking-tighter">${item.price.toFixed(2)}</p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t border-white/5 mt-auto">
                    <button
                      onClick={() => onToggleItem(item.id)}
                      className={`text-[9px] font-black tracking-[0.1em] px-4 py-1.5 rounded-full border transition-all ${item.available ? 'text-green-500 border-green-500/20 bg-green-500/5' : 'text-red-500 border-red-500/20 bg-red-500/5'}`}
                    >
                      {item.available ? 'ONLINE' : 'PAUSED'}
                    </button>

                    <div className="flex gap-2">
                      <button
                        title="Edit Item"
                        onClick={() => openEditForm(item)}
                        className="p-3 rounded-xl bg-white/5 hover:bg-amber-500 hover:text-black transition-all border border-white/5"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                      </button>
                      <button
                        title="Delete Item"
                        onClick={() => handleDelete(item.id)}
                        className="p-3 rounded-xl bg-white/5 hover:bg-red-500 text-red-500 hover:text-white transition-all border border-white/5"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="glass-panel p-10 rounded-[2.5rem] border border-white/10 max-w-2xl mx-auto shadow-2xl relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 honey-gradient opacity-50"></div>
              <div className="flex justify-between items-center mb-8">
                <h3 className="text-2xl font-black tracking-tight uppercase">{editingItem ? 'Update Item' : 'Create Item'}</h3>
                <button onClick={() => setIsFormOpen(false)} className="text-white/20 hover:text-white uppercase text-[10px] font-black tracking-[0.2em] transition-colors">Discard</button>
              </div>

              <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2 col-span-2">
                  <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">Item Title</label>
                  <input
                    required
                    value={formData.name}
                    onChange={e => setFormData({ ...formData, name: e.target.value })}
                    placeholder="e.g. Signature Truffle Fries"
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-4 outline-none focus:border-amber-500 transition-all"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">Category</label>
                  <input
                    required
                    value={formData.category}
                    onChange={e => setFormData({ ...formData, category: e.target.value })}
                    placeholder="BURGERS, APPETIZERS, etc."
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-4 outline-none focus:border-amber-500"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">Price ($)</label>
                  <input
                    required
                    type="number"
                    step="0.01"
                    value={formData.price}
                    onChange={e => setFormData({ ...formData, price: e.target.value })}
                    placeholder="0.00"
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-4 outline-none focus:border-amber-500"
                  />
                </div>
                <div className="space-y-2 col-span-2">
                  <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">Image URL</label>
                  <input
                    required
                    value={formData.image}
                    onChange={e => setFormData({ ...formData, image: e.target.value })}
                    placeholder="https://images.unsplash.com/..."
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-4 outline-none focus:border-amber-500"
                  />
                </div>
                <div className="space-y-2 col-span-2">
                  <label className="text-[10px] font-black text-white/30 uppercase tracking-[0.2em]">Description</label>
                  <textarea
                    required
                    value={formData.description}
                    onChange={e => setFormData({ ...formData, description: e.target.value })}
                    placeholder="Describe the flavor profile..."
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-5 py-4 outline-none focus:border-amber-500 h-32 resize-none"
                  />
                </div>
                <button type="submit" className="col-span-2 honey-gradient py-5 rounded-2xl text-black font-black text-sm uppercase tracking-[0.2em] shadow-xl shadow-amber-500/20 active:scale-[0.98] transition-all">
                  {editingItem ? 'Commit Changes' : 'Confirm Entry'}
                </button>
              </form>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;