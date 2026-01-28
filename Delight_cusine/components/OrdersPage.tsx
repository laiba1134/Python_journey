
import React from 'react';
import { Order, OrderStatus } from '../types';

interface OrdersPageProps {
  orders: Order[];
}

const OrdersPage: React.FC<OrdersPageProps> = ({ orders }) => {
  if (orders.length === 0) {
    return (
      <div className="py-20 text-center space-y-6">
        <h2 className="text-3xl font-bold">No orders yet.</h2>
        <p className="text-white/40">Hungry? Our kitchen is waiting for your signal.</p>
      </div>
    );
  }

  const getStatusColor = (status: OrderStatus) => {
    switch (status) {
      case OrderStatus.PLACED: return 'text-amber-500';
      case OrderStatus.PREPARING: return 'text-blue-400';
      case OrderStatus.OUT_FOR_DELIVERY: return 'text-purple-400';
      case OrderStatus.DELIVERED: return 'text-green-500';
      default: return 'text-white/40';
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <h2 className="text-3xl font-bold">Live Tracking & History</h2>
      {orders.map(order => (
        <div key={order.id} className="glass-panel rounded-3xl overflow-hidden border border-white/5">
          <div className="bg-white/5 px-8 py-4 flex justify-between items-center border-b border-white/5">
            <div>
              <p className="text-xs text-white/40 font-bold uppercase">Order ID</p>
              <p className="font-mono font-bold">#{order.id.toUpperCase()}</p>
            </div>
            <div className="text-right">
              <p className="text-xs text-white/40 font-bold uppercase">Status</p>
              <p className={`font-black tracking-tight ${getStatusColor(order.status)}`}>{order.status.toUpperCase()}</p>
            </div>
          </div>

          <div className="p-8 grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <h3 className="text-sm font-bold text-white/40 uppercase">Order Details</h3>
              <div className="space-y-2">
                {order.items.map(i => (
                  <div key={i.id} className="flex justify-between text-sm">
                    <span className="text-white/80">{i.menuItem.name} <span className="text-white/30">x{i.quantity}</span></span>
                    <span>${(i.menuItem.price * i.quantity).toFixed(2)}</span>
                  </div>
                ))}
                <div className="pt-2 mt-2 border-t border-white/5 flex justify-between font-bold">
                  <span>Grand Total</span>
                  <span className="honey-text">${order.total.toFixed(2)}</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-sm font-bold text-white/40 uppercase">Logistics</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-white/40">Placed At</span>
                  <span>{order.timestamp}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/40">Mode</span>
                  <span>{order.orderMode}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-white/40">Payment</span>
                  <span>{order.paymentMethod}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="px-8 pb-8">
            <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden flex">
              <div className={`h-full bg-amber-500 transition-all duration-1000 ${order.status === OrderStatus.PLACED ? 'w-1/4' : order.status === OrderStatus.PREPARING ? 'w-1/2' : order.status === OrderStatus.OUT_FOR_DELIVERY ? 'w-3/4' : 'w-full'}`}></div>
            </div>
            <div className="flex justify-between text-[10px] font-bold text-white/20 mt-2 uppercase tracking-tighter">
              <span>Placed</span>
              <span>Prep</span>
              <span>Transit</span>
              <span>Done</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default OrdersPage;
