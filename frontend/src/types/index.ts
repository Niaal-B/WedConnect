export interface User {
  id: string;
  email: string;
  name?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  name?: string;
}

export interface Vendor {
  id: string;
  name: string;
  category?: string;
  // Extend when backend schema is known
}
