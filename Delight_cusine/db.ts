
import { User, MenuItem, Order, UserRole } from './types';

const DEFAULT_ADMIN: User = {
  id: 'admin-001',
  email: 'admin123@gmail.com',
  password: 'admin1234',
  role: UserRole.ADMIN
};

export const db = {
  getUsers: (): User[] => {
    const users = localStorage.getItem('db_users');
    return users ? JSON.parse(users) : [DEFAULT_ADMIN];
  },
  
  saveUser: (user: User) => {
    const users = db.getUsers();
    users.push(user);
    localStorage.setItem('db_users', JSON.stringify(users));
  },

  findUserByEmail: (email: string): User | undefined => {
    return db.getUsers().find(u => u.email.toLowerCase() === email.toLowerCase());
  },

  getMenu: (): MenuItem[] => {
    const menu = localStorage.getItem('db_menu');
    return menu ? JSON.parse(menu) : [];
  },

  saveMenu: (items: MenuItem[]) => {
    localStorage.setItem('db_menu', JSON.stringify(items));
  },

  deleteMenuItem: (id: string) => {
    // Standard delete: filters out and persists
    const menu = db.getMenu();
    const updated = menu.filter(item => item.id !== id);
    db.saveMenu(updated);
    return updated;
  },

  getOrders: (): Order[] => {
    const orders = localStorage.getItem('db_orders');
    return orders ? JSON.parse(orders) : [];
  },

  saveOrder: (order: Order) => {
    const orders = db.getOrders();
    orders.unshift(order);
    localStorage.setItem('db_orders', JSON.stringify(orders));
  },

  updateOrderStatus: (orderId: string, status: string) => {
    const orders = db.getOrders();
    const updated = orders.map(o => o.id === orderId ? { ...o, status: status as any } : o);
    localStorage.setItem('db_orders', JSON.stringify(updated));
  }
};
