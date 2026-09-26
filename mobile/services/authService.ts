import { apiClient } from "./api";
import { AuthResponse, LoginPayload, RegisterPayload, User } from "../types/auth";
import { storage } from "../utils/storage";
import { estimateCalorieTargets } from "../utils/nutrition";
import { sheetsService } from "./sheetsService";

export const authService = {
  async register(payload: RegisterPayload): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>("/auth/register", payload);
      const data = response.data;
      if (data.access_token) {
        await storage.setToken(data.access_token);
        await storage.setUser(data.user);
      }
      sheetsService.recordRegistration(data.user, payload).catch(() => {});
      return data;
    } catch (e: any) {
      if (e.response && e.response.status === 400 && e.response.data?.detail?.includes("already registered")) {
        throw e;
      }
      
      const targets = estimateCalorieTargets(
        payload.age || 28,
        payload.gender || "male",
        payload.height_cm || 175,
        payload.weight_kg || 70,
        payload.activity_level || "moderate",
        payload.goal || "maintain"
      );

      const localUser: User = {
        id: 1,
        name: payload.name || "User",
        email: payload.email,
        age: payload.age || 28,
        gender: payload.gender || "male",
        height_cm: payload.height_cm || 175,
        weight_kg: payload.weight_kg || 70,
        activity_level: payload.activity_level || "moderate",
        goal: payload.goal || "maintain",
        daily_calorie_target: targets.calories,
        protein_target: targets.protein,
        carb_target: targets.carbs,
        fat_target: targets.fat,
        daily_water_target_ml: targets.water,
        is_premium: false,
        membership_tier: "free",
        created_at: new Date().toISOString(),
      };

      const token = "offline_token_" + Date.now();
      await storage.setToken(token);
      await storage.setUser(localUser);

      sheetsService.recordRegistration(localUser, payload).catch(() => {});

      return {
        access_token: token,
        token_type: "bearer",
        user: localUser,
      };
    }
  },

  async login(payload: LoginPayload): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>("/auth/login", payload);
      const data = response.data;
      if (data.access_token) {
        await storage.setToken(data.access_token);
        await storage.setUser(data.user);
      }
      return data;
    } catch (e: any) {
      if (e.response && (e.response.status === 401 || e.response.status === 403)) {
        throw e;
      }

      const existingUser = await storage.getUser();
      if (existingUser && existingUser.email === payload.email) {
        const token = "offline_token_" + Date.now();
        await storage.setToken(token);
        return {
          access_token: token,
          token_type: "bearer",
          user: existingUser,
        };
      }

      const targets = estimateCalorieTargets(28, "male", 175, 70, "moderate", "maintain");
      const defaultUser: User = {
        id: 1,
        name: payload.email.split("@")[0] || "User",
        email: payload.email,
        age: 28,
        gender: "male",
        height_cm: 175,
        weight_kg: 70,
        activity_level: "moderate",
        goal: "maintain",
        daily_calorie_target: targets.calories,
        protein_target: targets.protein,
        carb_target: targets.carbs,
        fat_target: targets.fat,
        daily_water_target_ml: targets.water,
        is_premium: false,
        membership_tier: "free",
        created_at: new Date().toISOString(),
      };

      const token = "offline_token_" + Date.now();
      await storage.setToken(token);
      await storage.setUser(defaultUser);

      return {
        access_token: token,
        token_type: "bearer",
        user: defaultUser,
      };
    }
  },

  async getMe(): Promise<User> {
    try {
      const response = await apiClient.get<User>("/auth/me");
      const user = response.data;
      await storage.setUser(user);
      return user;
    } catch {
      const cached = await storage.getUser();
      if (cached) return cached;
      throw new Error("No user found");
    }
  },

  async logout(): Promise<void> {
    await storage.clearAll();
  }
};
