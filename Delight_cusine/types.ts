export enum UserRole {
  ADMIN = 'ADMIN',
  CUSTOMER = 'CUSTOMER'
}

export enum OrderStatus {
  PLACED = 'Order Placed',
  PREPARING = 'Preparing',
  OUT_FOR_DELIVERY = 'Out for Delivery',
  DELIVERED = 'Delivered'
}

export enum PaymentMethod {
  CARD = 'Card',
  COD = 'Cash on Delivery'
}

export enum OrderMode {
  DELIVERY = 'Delivery',
  PICKUP = 'Pickup'
}

export interface User {
  id: string;
  email: string;
  password?: string;
  role: UserRole;
}

export interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  is_available: boolean;
  is_deleted?: boolean; // Soft delete support
  image_url: string;
}

export interface CartItem {
  id: string;
  menuItem: MenuItem;
  quantity: number;
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
