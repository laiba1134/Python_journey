import { User, MenuItem, Order, RestaurantStatus, OrderStatus } from './types';

// Flask backend API URL
const API_BASE_URL = 'http://localhost:5000/api';

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
      // Special handling for is_deleted - keep it as is
      if (key === 'is_deleted') {
        acc['is_deleted'] = obj[key];
      } else {
        const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
        acc[camelKey] = toCamelCase(obj[key]);
      }
      return acc;
    }, {} as any);
  }
  return obj;
}

// Helper function for API calls
async function apiCall(endpoint: string, options: RequestInit = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      console.error('API Error:', error);
      throw new Error(error.detail || 'Request failed');
    }

    const data = await response.json();
    console.log('API Response:', data); // Debug log
    return data;
  } catch (error) {
    console.error('Fetch Error:', error);
    throw error;
  }
}

export const db = {
  // Authentication
  async login(username: string, password: string): Promise<User | null> {
    try {
      console.log('Attempting login with:', { username, password: '***' }); // Debug log
      const response = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      });
      console.log('Raw API response:', response); // Debug log

      // Convert snake_case to camelCase
      const user = toCamelCase(response);
      console.log('Converted user:', user); // Debug log
      console.log('User role:', user.role, 'Type:', typeof user.role); // Debug log

      return user;
    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed: ' + (error as Error).message);
      return null;
    }
  },

  async register(username: string, email: string, password: string, role: string = 'customer'): Promise<User | null> {
    try {
      console.log('Attempting registration with:', { username, email, role }); // Debug log
      const user = await apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ username, email, password, role }),
      });
      console.log('Registration successful:', user); // Debug log
      // Convert snake_case to camelCase
      return toCamelCase(user);
    } catch (error) {
      console.error('Registration failed:', error);
      alert('Registration failed: ' + (error as Error).message);
      return null;
    }
  },

  // Menu operations
  async getMenu(includeDeleted: boolean = false): Promise<MenuItem[]> {
    try {
      const queryParam = includeDeleted ? '?include_deleted=true' : '';
      const data = await apiCall(`/menu${queryParam}`);
      console.log('Raw menu data:', data);

      // Handle different response formats
      let menuArray = data;
      if (data && typeof data === 'object' && !Array.isArray(data)) {
        // If it's an object, look for common array properties
        menuArray = data.items || data.menu_items || data.data || [];
      }

      const converted = toCamelCase(menuArray);
      console.log('Converted menu items:', converted);
      return Array.isArray(converted) ? converted : [];
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

  async updateMultipleMenuItems(items: MenuItem[]): Promise<void> {
    try {
      console.log('Updating multiple items:', items.length);
      console.log('Items being sent (before conversion):', items);

      // Don't convert - send items as-is since MenuItem already has the right format
      const response = await apiCall('/menu/batch', {
        method: 'PUT',
        body: JSON.stringify(items),
      });

      console.log('Batch update response:', response);
    } catch (error) {
      console.error('Failed to batch update menu items:', error);
      throw error;
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

  async deleteMenuItem(itemId: string): Promise<void> {
    try {
      await apiCall(`/menu/${itemId}`, {
        method: 'DELETE',
      });
      console.log(`Successfully deleted item ${itemId}`);
    } catch (error) {
      console.error('Failed to delete menu item:', error);
      throw error;
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
      const data = await apiCall('/restaurant/status');
      console.log('Restaurant status from API:', data);
      const converted = toCamelCase(data);
      console.log('Restaurant status converted:', converted);
      return converted;
    } catch (error) {
      console.error('Failed to fetch restaurant status:', error);
      return { isOpen: true };
    }
  },

  async saveRestaurantStatus(status: RestaurantStatus): Promise<void> {
    try {
      console.log('Saving restaurant status:', status);
      await apiCall('/restaurant/status', {
        method: 'PUT',
        body: JSON.stringify(toSnakeCase(status)),
      });
    } catch (error) {
      console.error('Failed to save restaurant status:', error);
    }
  },
};