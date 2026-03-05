import { apiClient } from "./client";

export async function getVendors() {
  // Stub until backend GET /api/vendors is ready
  const { data } = await apiClient.get("/api/vendors");
  return data;
}
