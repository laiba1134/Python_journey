import { User, MenuItem, Order, RestaurantStatus, OrderStatus } from './types';

// Flask backend API URL
const API_BASE_URL = 'http://localhost:5000/api';

// Store auth token - use a simple in-memory variable with localStorage backup
let authToken: string | null = null;

// Initialize token from localStorage on module load
if (typeof window !== 'undefined') {
  authToken = localStorage.getItem('auth_token');
  console.log('Token loaded from localStorage:', authToken ? 'Found' : 'Not found');
}

export function setAuthToken(token: string | null) {
  console.log('Setting auth token:', token ? 'Token set' : 'Token cleared');
  authToken = token;
  if (token) {
    localStorage.setItem('auth_token', token);
  } else {
    localStorage.removeItem('auth_token');
  }
}

export function getAuthToken(): string | null {
  // Always check localStorage in case it was updated
  if (!authToken && typeof window !== 'undefined') {
    authToken = localStorage.getItem('auth_token');
  }
  console.log('Getting auth token:', authToken ? 'Token exists' : 'No token');
  return authToken;
}

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
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Add auth token if available
    const token = getAuthToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
      console.log('✅ Auth token added to request');
    } else {
      console.warn('⚠️ No auth token available for request to:', endpoint);
    }

    console.log('API Call:', {
      endpoint,
      method: options.method || 'GET',
      hasToken: !!token
    });

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      console.error('API Error:', error);
      console.error('Status:', response.status);
      console.error('Endpoint:', endpoint);
      throw new Error(error.detail || error.message || 'Request failed');
    }

    const data = await response.json();
    console.log('API Response:', data);
    return data;
  } catch (error) {
    console.error('Fetch Error:', error);
    throw error;
  }
}

export const db = {
  // Authentication
  async login(email: string, password: string): Promise<User | null> {
    try {
      console.log('🔐 Attempting login with:', { email });

      const response = await apiCall('/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          email,
          password
        }),
      });

      console.log('✅ Login successful, response:', response);

      // Store the token FIRST
      if (response.access_token) {
        console.log('💾 Storing auth token...');
        setAuthToken(response.access_token);
        console.log('✅ Token stored successfully');
      } else {
        console.error('⚠️ No access token in response!');
      }

      // Return the user object
      if (response.user) {
        const user = {
          ...response.user,
          role: response.role || response.user.role
        };
        console.log('👤 User logged in:', user);
        return user;
      }

      return null;
    } catch (error) {
      console.error('❌ Login failed:', error);
      return null;
    }
  },

  async register(username: string, email: string, password: string, role: string = 'customer'): Promise<User | null> {
    try {
      console.log('Attempting registration with:', { username, email, role });
      const response = await apiCall('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ username, email, password, role }),
      });

      console.log('Registration response:', response);

      // Store the token
      if (response.access_token) {
        setAuthToken(response.access_token);
      }

      // Return the user object
      return response.user || null;
    } catch (error) {
      console.error('Registration failed:', error);
      return null;
    }
  },

  logout() {
    console.log('🚪 Logging out, clearing token');
    setAuthToken(null);
  },

  // Check if user is logged in
  isAuthenticated(): boolean {
    const token = getAuthToken();
    const isAuth = !!token;
    console.log('🔍 Checking auth status:', isAuth ? 'Authenticated' : 'Not authenticated');
    return isAuth;
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
        menuArray = data.items || data.menu_items || data.data || [];
      }

      const converted = toCamelCase(menuArray);

      // Ensure all IDs are strings
      const withStringIds = Array.isArray(converted)
        ? converted.map((item: any) => ({
          ...item,
          id: String(item.id)
        }))
        : [];

      console.log('Converted menu items:', withStringIds);
      return withStringIds;
    } catch (error) {
      console.error('Failed to fetch menu:', error);
      return [];
    }
  },

  async addMenuItem(item: Omit<MenuItem, 'id'>): Promise<void> {
    try {
      await apiCall('/menu', {
        method: 'POST',
        body: JSON.stringify(toSnakeCase(item)),
      });
    } catch (error) {
      console.error('Failed to add menu item:', error);
      throw error;
    }
  },

  async updateMenuItem(item: MenuItem): Promise<void> {
    try {
      // Convert string ID to number for API call if needed
      const itemId = typeof item.id === 'string' ? item.id : String(item.id);

      await apiCall(`/menu/${itemId}`, {
        method: 'PUT',
        body: JSON.stringify(toSnakeCase(item)),
      });
    } catch (error) {
      console.error('Failed to update menu item:', error);
      throw error;
    }
  },

  async updateMultipleMenuItems(items: MenuItem[]): Promise<void> {
    try {
      console.log('Updating multiple menu items:', items.length);

      // Update each item individually since we don't have a batch endpoint
      const updatePromises = items.map(item => {
        const itemId = typeof item.id === 'string' ? item.id : String(item.id);
        return apiCall(`/menu/${itemId}`, {
          method: 'PUT',
          body: JSON.stringify(toSnakeCase(item)),
        });
      });

      await Promise.all(updatePromises);
      console.log('All items updated successfully');
    } catch (error) {
      console.error('Failed to update multiple menu items:', error);
      throw error;
    }
  },

  async toggleItemAvailability(itemId: string): Promise<void> {
    try {
      // Get the current item
      const items = await this.getMenu(true);
      const item = items.find(i => String(i.id) === String(itemId));

      if (item) {
        await apiCall(`/menu/${itemId}`, {
          method: 'PUT',
          body: JSON.stringify({ available: !item.available }),
        });
      }
    } catch (error) {
      console.error('Failed to toggle item availability:', error);
      throw error;
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
      const endpoint = userId ? `/orders?user_id=${userId}` : '/orders';
      const data = await apiCall(endpoint);

      // Handle response format
      let ordersArray = data;
      if (data && typeof data === 'object' && !Array.isArray(data)) {
        ordersArray = data.orders || data.data || [];
      }

      // Ensure all IDs are strings
      const withStringIds = Array.isArray(ordersArray)
        ? ordersArray.map((order: any) => ({
          ...order,
          id: String(order.id),
          items: order.items?.map((item: any) => ({
            ...item,
            id: String(item.id),
            menuItem: {
              ...item.menuItem,
              id: String(item.menuItem?.id || item.menu_item_id)
            }
          })) || []
        }))
        : [];

      return withStringIds;
    } catch (error) {
      console.error('Failed to fetch orders:', error);
      return [];
    }
  },

  async saveOrder(order: any): Promise<void> {
    try {
      const orderData = {
        items: order.items.map((item: any) => ({
          menu_item_id: item.menuItem.id,
          quantity: item.quantity,
        })),
        delivery_address: order.deliveryAddress || order.delivery_address,
        notes: order.notes || '',
        order_mode: order.orderMode || order.order_mode || 'Delivery',
        payment_method: order.paymentMethod || order.payment_method || 'Cash on Delivery',
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
      throw error;
    }
  },

  // Restaurant status operations
  async getRestaurantStatus(): Promise<any> {
    try {
      const data = await apiCall('/restaurant/status');
      console.log('Restaurant status from API:', data);
      return {
        isOpen: data.isOpen ?? true,
        message: data.message || ''
      };
    } catch (error) {
      console.error('Failed to fetch restaurant status:', error);
      return { isOpen: true, message: '' };
    }
  },

  async saveRestaurantStatus(status: any): Promise<void> {
    try {
      console.log('Saving restaurant status:', status);
      await apiCall('/restaurant/status', {
        method: 'PUT',
        body: JSON.stringify({
          is_open: status.isOpen,
          message: status.message || ''
        }),
      });
    } catch (error) {
      console.error('Failed to save restaurant status:', error);
      throw error;
    }
  },

  async toggleRestaurantStatus(): Promise<void> {
    try {
      await apiCall('/restaurant/toggle', {
        method: 'POST',
      });
    } catch (error) {
      console.error('Failed to toggle restaurant status:', error);
      throw error;
    }
  },
};