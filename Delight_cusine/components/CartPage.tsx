
import React, { useState } from 'react';
import { CartItem, PaymentMethod, OrderMode } from '../types';

interface CartPageProps {
  cart: CartItem[];
  onRemove: (id: string) => void;
  onCheckout: (payment: PaymentMethod, mode: OrderMode) => void;
  isClosed: boolean;
}

const CartPage: React.FC<CartPageProps> = ({ cart, onRemove, onCheckout, isClosed }) => {
  const [payment, setPayment] = useState<PaymentMethod>(PaymentMethod.CARD);
  const [mode, setMode] = useState<OrderMode>(OrderMode.DELIVERY);

  const subtotal = cart.reduce((acc, i) => acc + (i.menuItem.price * i.quantity), 0);
  const fee = mode === OrderMode.DELIVERY ? 5.00 : 0;
  const total = subtotal + fee;

  if (cart.length === 0) {
    return (
      <div className="py-20 text-center space-y-6">
        <div className="text-6xl">🐝</div>
        <h2 className="text-3xl font-bold">Your cart is as empty as a winter hive.</h2>
        <p className="text-white/40">Add some golden dishes to get started.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
      <div className="lg:col-span-2 space-y-4">
        <h2 className="text-2xl font-bold mb-6">Your Selection</h2>
        {cart.map(item => (
          <div key={item.id} className="glass-panel p-4 rounded-2xl flex gap-4 items-center">
            <img src={item.menuItem.image_url} className="w-20 h-20 object-cover rounded-lg" />
            <div className="flex-grow">
              <h3 className="font-bold">{item.menuItem.name}</h3>
              <p className="text-sm text-white/40">Quantity: {item.quantity}</p>
            </div>
            <div className="text-right">
              <p className="font-bold honey-text">${(item.menuItem.price * item.quantity).toFixed(2)}</p>
              <button onClick={() => onRemove(item.id)} className="text-xs text-red-400 hover:text-red-300 transition-colors mt-2">Remove</button>
            </div>
          </div>
        ))}
      </div>

      <div className="space-y-6">
        <div className="glass-panel p-6 rounded-3xl space-y-6 sticky top-24">
          <h2 className="text-xl font-bold">Order Summary</h2>

          <div className="space-y-3">
            <div className="flex justify-between text-white/60">
              <span>Subtotal</span>
              <span>${subtotal.toFixed(2)}</span>
            </div>
            <div className="flex justify-between text-white/60">
              <span>{mode} Fee</span>
              <span>${fee.toFixed(2)}</span>
            </div>
            <div className="h-px bg-white/10 my-2"></div>
            <div className="flex justify-between text-xl font-bold">
              <span>Total</span>
              <span className="honey-text">${total.toFixed(2)}</span>
            </div>
          </div>

          <div className="space-y-4">
            <label className="text-xs font-bold text-white/40 uppercase tracking-widest">Order Mode</label>
            <div className="flex gap-2">
              {[OrderMode.DELIVERY, OrderMode.PICKUP].map(m => (
                <button
                  key={m}
                  onClick={() => setMode(m)}
                  className={`flex-grow py-2 rounded-lg text-sm font-bold border ${mode === m ? 'bg-amber-500 border-amber-500 text-black' : 'border-white/10 text-white/60'}`}
                >
                  {m}
                </button>
              ))}
            </div>
          </div>

          <div className="space-y-4">
            <label className="text-xs font-bold text-white/40 uppercase tracking-widest">Payment Method</label>
            <div className="flex gap-2">
              {[PaymentMethod.CARD, PaymentMethod.COD].map(p => (
                <button
                  key={p}
                  onClick={() => setPayment(p)}
                  className={`flex-grow py-2 rounded-lg text-sm font-bold border ${payment === p ? 'bg-amber-500 border-amber-500 text-black' : 'border-white/10 text-white/60'}`}
                >
                  {p === PaymentMethod.CARD ? 'Card' : 'Cash'}
                </button>
              ))}
            </div>
          </div>

          <button
            disabled={isClosed}
            onClick={() => onCheckout(payment, mode)}
            className={`w-full py-4 rounded-2xl font-black text-lg transition-all shadow-xl shadow-amber-500/20 ${isClosed ? 'bg-white/5 text-white/20 cursor-not-allowed' : 'honey-gradient text-black hover:scale-[1.02]'}`}
          >
            {isClosed ? 'CUISINE CLOSED' : 'PLACE ORDER'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default CartPage;
