import { apiClient } from "./client";
import type { LoginCredentials, RegisterPayload } from "@/types";

export async function login(credentials: LoginCredentials) {
  // Stub until backend POST /api/login is ready
  const { data } = await apiClient.post("/api/login", credentials);
  return data;
}

export async function register(payload: RegisterPayload) {
  // Stub until backend POST /api/register is ready
  const { data } = await apiClient.post("/api/register", payload);
  return data;
}
