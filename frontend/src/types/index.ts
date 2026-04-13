export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AdminLoginCredentials {
  username: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  name?: string;
}

export interface Vendor {
  id: number;
  name: string;
  email: string;
  contact_number: string;
  alternative_number?: string;
  whatsapp_number: string;
  years_of_experience: number;
  instagram_url?: string;
  category?: number | string;
  districts?: number[];
  joining_date: string;
  is_active: boolean;
}

export interface Category {
  id: number;
  name: string;
  is_active: boolean;
}

export interface District {
  id: number;
  name: string;
  state: number;
  state_name: string;
}

export interface CreateVendorPayload {
  name: string;
  email: string;
  contact_number: string;
  alternative_number?: string;
  whatsapp_number: string;
  years_of_experience: number;
  instagram_url?: string;
  category?: number;
  districts?: number[];
}

export interface BookingSlot {
  start_time: string;
  end_time: string;
}

export interface BookingDate {
  event_date: string;
  slots: BookingSlot[];
}

export interface Booking {
  id: number;
  customer_name: string;
  district: number | null;
  address: string;
  phone_number: string;
  alternative_phone_number?: string;
  map_url?: string;
  total_amount: string;
  advance_amount: string;
  created_at: string;
  is_deleted: boolean;
  total_paid: number;
  balance_amount: number;
  payment_status: "NOT_PAID" | "PARTIAL" | "PAID";
  event_status: "TODAY" | "UPCOMING" | "PAST" | "UNKNOWN";
  dates: BookingDate[];
}

export interface CreateBookingPayload {
  customer_name: string;
  district?: number;
  address: string;
  phone_number: string;
  alternative_phone_number?: string;
  map_url?: string;
  total_amount: number;
  advance_amount: number;
  dates: BookingDate[];
}
