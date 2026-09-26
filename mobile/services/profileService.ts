import { apiClient } from "./api";
import { User } from "../types/auth";
import { storage } from "../utils/storage";

export const profileService = {
  async getProfile(): Promise<User> {
    try {
      const response = await apiClient.get<User>("/profile");
      await storage.setUser(response.data);
      return response.data;
    } catch {
      const cached = await storage.getUser();
      if (cached) return cached;
      throw new Error("No profile found");
    }
  },

  async updateProfile(payload: Partial<User>): Promise<User> {
    try {
      const response = await apiClient.put<User>("/profile", payload);
      await storage.setUser(response.data);
      return response.data;
    } catch {
      const cached = (await storage.getUser()) || ({} as User);
      const updated: User = { ...cached, ...payload };
      await storage.setUser(updated);
      return updated;
    }
  },

  async updateGoals(goals: {
    daily_calorie_target?: number;
    protein_target?: number;
    carb_target?: number;
    fat_target?: number;
    daily_water_target_ml?: number;
  }): Promise<User> {
    try {
      const response = await apiClient.put<User>("/profile/goals", goals);
      await storage.setUser(response.data);
      return response.data;
    } catch {
      const cached = (await storage.getUser()) || ({} as User);
      const updated: User = { ...cached, ...goals };
      await storage.setUser(updated);
      return updated;
    }
  }
};
