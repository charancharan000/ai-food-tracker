import { apiClient } from "./api";
import { User } from "../types/auth";

export const profileService = {
  async getProfile(): Promise<User> {
    const response = await apiClient.get<User>("/profile");
    return response.data;
  },

  async updateProfile(payload: Partial<User>): Promise<User> {
    const response = await apiClient.put<User>("/profile", payload);
    return response.data;
  },

  async updateGoals(goals: {
    daily_calorie_target?: number;
    protein_target?: number;
    carb_target?: number;
    fat_target?: number;
    daily_water_target_ml?: number;
  }): Promise<User> {
    const response = await apiClient.put<User>("/profile/goals", goals);
    return response.data;
  }
};
