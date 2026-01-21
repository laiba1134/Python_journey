import { User, MenuItem, Order, RestaurantStatus, OrderStatus } from './types';

const API_BASE_URL = 'http://localhost:8000/api';

// Helper to handle camelCase to snake_case conversion
function toSnakeCase(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(toSnakeCase);
  } else if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj).reduce((acc, key) => {
      const snakeKey = key.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
      acc[snakeKey] = toSnakeCase(obj[key]);
      return acc;
    }, {} as any);
  }
  return obj;
}

// Helper to handle snake_case to camelCase conversion
function toCamelCase(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(toCamelCase);
  } else if (obj !== null && typeof obj === 'object') {
    return Object.keys(obj).reduce((acc, key) => {
      const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
      acc[camelKey] = toCamelCase(obj[key]);
      return acc;
    }, {} as any);
  }
  return obj;
}

// Helper function for API calls
async function apiCall(endpoint: string, options: RequestInit = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || 'Request failed');
  }

  return response.json();
}

export const db = {
  // Authentication
  async login(username: string, password: string): Promise<User | null> {
    try {
      const user = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      });
      return user;
    } catch (error) {
      console.error('Login failed:', error);
      return null;
    }
  },

  async register(username: string, password: string, role: string): Promise<User | null> {
    try {
      const user = await apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ username, password, role }),
      });
      return user;
    } catch (error) {
      console.error('Registration failed:', error);
      return null;
    }
  },

  // Menu operations
  async getMenu(): Promise<MenuItem[]> {
    try {
      const data = await apiCall('/menu');
      return toCamelCase(data);
    } catch (error) {
      console.error('Failed to fetch menu:', error);
      return [];
    }
  },

  async updateMenuItem(item: MenuItem): Promise<void> {
    try {
      await apiCall(`/menu/${item.id}`, {
        method: 'PUT',
        body: JSON.stringify(toSnakeCase(item)),
      });
    } catch (error) {
      console.error('Failed to update menu item:', error);
    }
  },

  async toggleItemAvailability(itemId: string): Promise<void> {
    try {
      await apiCall(`/menu/${itemId}/toggle`, {
        method: 'PATCH',
      });
    } catch (error) {
      console.error('Failed to toggle item availability:', error);
    }
  },

  // Order operations
  async getOrders(userId?: string): Promise<Order[]> {
    try {
      const queryParam = userId ? `?user_id=${userId}` : '';
      const data = await apiCall(`/orders${queryParam}`);
      return toCamelCase(data);
    } catch (error) {
      console.error('Failed to fetch orders:', error);
      return [];
    }
  },

  async saveOrder(order: Order): Promise<void> {
    try {
      // Transform order items to match backend schema
      const orderData = {
        user_id: order.userId,
        items: order.items.map(item => ({
          id: item.id,
          menu_item_id: item.menuItem.id,
          quantity: item.quantity,
          price_at_time: item.menuItem.price,
        })),
        total: order.total,
        status: order.status,
        payment_method: order.paymentMethod,
        order_mode: order.orderMode,
      };

      await apiCall('/orders', {
        method: 'POST',
        body: JSON.stringify(orderData),
      });
    } catch (error) {
      console.error('Failed to save order:', error);
      throw error;
    }
  },

  async updateOrderStatus(orderId: string, status: OrderStatus): Promise<void> {
    try {
      await apiCall(`/orders/${orderId}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status }),
      });
    } catch (error) {
      console.error('Failed to update order status:', error);
    }
  },

  // Restaurant status operations
  async getRestaurantStatus(): Promise<RestaurantStatus> {
    try {
      return await apiCall('/restaurant/status');
    } catch (error) {
      console.error('Failed to fetch restaurant status:', error);
      return { isOpen: true };
    }
  },

  async saveRestaurantStatus(status: RestaurantStatus): Promise<void> {
    try {
      await apiCall('/restaurant/status', {
        method: 'PUT',
        body: JSON.stringify({ is_open: status.isOpen }),
      });
    } catch (error) {
      console.error('Failed to save restaurant status:', error);
    }
  },
};