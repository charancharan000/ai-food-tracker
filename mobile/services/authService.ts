import { apiClient } from "./api";
import { AuthResponse, LoginPayload, RegisterPayload, User } from "../types/auth";
import { storage } from "../utils/storage";

export const authService = {
  async register(payload: RegisterPayload): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>("/auth/register", payload);
    const data = response.data;
    if (data.access_token) {
      await storage.setToken(data.access_token);
      await storage.setUser(data.user);
    }
    return data;
  },

  async login(payload: LoginPayload): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>("/auth/login", payload);
    const data = response.data;
    if (data.access_token) {
      await storage.setToken(data.access_token);
      await storage.setUser(data.user);
    }
    return data;
  },

  async getMe(): Promise<User> {
    const response = await apiClient.get<User>("/auth/me");
    const user = response.data;
    await storage.setUser(user);
    return user;
  },

  async logout(): Promise<void> {
    await storage.clearAll();
  }
};
