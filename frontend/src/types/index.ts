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
  whatsapp_number: string;
  years_of_experience: number;
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
  whatsapp_number: string;
  years_of_experience: number;
  category?: number;
  districts?: number[];
}
