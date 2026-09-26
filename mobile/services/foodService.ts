import { Platform } from "react-native";
import { apiClient } from "./api";
import { FoodAnalysisResponse, Meal, MealCreatePayload } from "../types/food";
import { localStore } from "../utils/localStorage";
import { storage } from "../utils/storage";

export const foodService = {
  async analyzeFood(imageUri: string, mimeType: string = "image/jpeg"): Promise<FoodAnalysisResponse> {
    try {
      const formData = new FormData();

      if (Platform.OS === "web") {
        const response = await fetch(imageUri);
        const blob = await response.blob();
        formData.append("file", blob, "food_photo.jpg");
      } else {
        const cleanUri = Platform.OS === "ios" ? imageUri.replace("file://", "") : imageUri;
        const filePayload: any = {
          uri: cleanUri,
          name: "food_photo.jpg",
          type: mimeType || "image/jpeg",
        };
        formData.append("file", filePayload);
      }

      const response = await apiClient.post<FoodAnalysisResponse>("/food/analyze", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        timeout: 10000,
      });

      return response.data;
    } catch {
      return localStore.getMockAnalysis();
    }
  },

  async createMeal(payload: MealCreatePayload): Promise<Meal> {
    try {
      const response = await apiClient.post<Meal>("/meals", payload);
      return response.data;
    } catch {
      const user = await storage.getUser();
      return await localStore.saveMeal(payload, user?.id || 1);
    }
  },

  async getTodayMeals(): Promise<Meal[]> {
    try {
      const response = await apiClient.get<Meal[]>("/meals/today");
      return response.data;
    } catch {
      const today = new Date().toISOString().split("T")[0];
      return await localStore.getMealsByDate(today);
    }
  },

  async getMealsByDate(dateStr: string): Promise<Meal[]> {
    try {
      const response = await apiClient.get<Meal[]>(`/meals?date=${dateStr}`);
      return response.data;
    } catch {
      return await localStore.getMealsByDate(dateStr);
    }
  },

  async getMealById(id: number): Promise<Meal> {
    try {
      const response = await apiClient.get<Meal>(`/meals/${id}`);
      return response.data;
    } catch {
      const meal = await localStore.getMealById(id);
      if (meal) return meal;
      throw new Error("Meal not found");
    }
  },

  async updateMeal(id: number, payload: Partial<MealCreatePayload>): Promise<Meal> {
    try {
      const response = await apiClient.put<Meal>(`/meals/${id}`, payload);
      return response.data;
    } catch {
      const updated = await localStore.updateMeal(id, payload);
      if (updated) return updated;
      throw new Error("Meal not found");
    }
  },

  async deleteMeal(id: number): Promise<void> {
    try {
      await apiClient.delete(`/meals/${id}`);
    } catch {
      await localStore.deleteMeal(id);
    }
  }
};
