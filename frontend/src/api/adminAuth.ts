import { apiClient } from "./client";
import type { AdminLoginCredentials } from "../types";

export async function adminLogin(credentials: AdminLoginCredentials) {
  const { data } = await apiClient.post("/api/v1/accounts/login/", credentials);
  return data;
}
