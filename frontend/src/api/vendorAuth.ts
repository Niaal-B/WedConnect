import { apiClient } from "./client";

export async function vendorLogin(credentials: { email: string; password: string }) {
  const { data } = await apiClient.post("/api/v1/vendors/login/", credentials);
  return data;
}
