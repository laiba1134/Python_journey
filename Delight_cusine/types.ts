// User types
export enum UserRole {
  ADMIN = 'ADMIN',
  CUSTOMER = 'CUSTOMER'
}

export interface User {
  id: number;
  email: string;
  name: string;
  role: string;
  createdAt?: string;
}

// Menu types
export interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  image: string;
  available: boolean;
  is_deleted?: boolean;
  createdAt?: string;
  updatedAt?: string;
}

// Cart types
export interface CartItem {
  id: string;
  menuItem: MenuItem;
  quantity: number;
}

// Order types
export enum OrderStatus {
  PLACED = "PLACED",
  PREPARING = "PREPARING",
  OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY",
  DELIVERED = "DELIVERED",
  CANCELLED = "CANCELLED"
}

export enum PaymentMethod {
  CASH = "Cash on Delivery",
  CARD = "Credit/Debit Card",
  ONLINE = "Online Payment"
}

export enum OrderMode {
  DELIVERY = "Delivery",
  PICKUP = "Pickup"
}

export interface OrderItem {
  id: string;
  quantity: number;
  menuItem: {
    id: string;
    name: string;
    price: number;
  };
}

export interface Order {
  id: string;
  userId?: number;
  status: OrderStatus;
  total: number;
  timestamp: string;
  orderMode: string;
  paymentMethod: string;
  deliveryAddress?: string;
  notes?: string;
  items: OrderItem[];
  createdAt?: string;
  updatedAt?: string;
}

// Restaurant status
export interface RestaurantStatus {
  isOpen: boolean;
  message?: string;
}