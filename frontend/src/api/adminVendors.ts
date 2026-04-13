import { apiClient } from "./client";
import type { Vendor, Category, District, CreateVendorPayload } from "../types";

export async function getVendors(): Promise<Vendor[]> {
  const { data } = await apiClient.get("/api/v1/vendors/vendors/");
  return data;
}

// Additional functions for Vendor ops
export async function activateVendor(id: number) {
  const { data } = await apiClient.patch(`/api/v1/vendors/vendors/${id}/activate/`);
  return data;
}

export async function deactivateVendor(id: number) {
  const { data } = await apiClient.patch(`/api/v1/vendors/vendors/${id}/deactivate/`);
  return data;
}

export async function getCategories(): Promise<Category[]> {
  const { data } = await apiClient.get("/api/v1/vendors/categories/");
  return data;
}

export async function getDistricts(): Promise<District[]> {
  const { data } = await apiClient.get("/api/v1/vendors/districts/");
  return data;
}

export async function createVendor(payload: CreateVendorPayload) {
  const { data } = await apiClient.post("/api/v1/vendors/vendors/create/", payload);
  return data;
}
