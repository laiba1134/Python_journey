export enum UserRole {
  ADMIN = 'admin',
  CUSTOMER = 'customer'
}

export interface User {
  id: string;
  username: string;
  email: string;
  role: UserRole | string; // Allow both enum and string
  createdAt: string;
}

export interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  image: string;
  available: boolean;
  is_deleted: boolean;
}

export interface CartItem {
  id: string;
  menuItem: MenuItem;
  quantity: number;
}

export enum OrderStatus {
  PLACED = "PLACED",
  PREPARING = "PREPARING",
  OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY",
  DELIVERED = "DELIVERED",
  CANCELLED = "CANCELLED"
}

export enum PaymentMethod {
  CASH = 'cash',
  CARD = 'card',
  ONLINE = 'online'
}

export enum OrderMode {
  DINE_IN = 'dine_in',
  TAKEAWAY = 'takeaway',
  DELIVERY = 'delivery'
}

export interface Order {
  id: string;
  userId: string;
  items: CartItem[];
  total: number;
  status: OrderStatus;
  paymentMethod: PaymentMethod;
  orderMode: OrderMode;
  timestamp: string;
}

export interface RestaurantStatus {
  isOpen: boolean;
}