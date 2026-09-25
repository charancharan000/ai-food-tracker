import { Platform } from "react-native";
import { apiClient } from "./api";
import { FoodAnalysisResponse, Meal, MealCreatePayload } from "../types/food";

export const foodService = {
  /**
   * Upload food photo using multipart/form-data to AI vision endpoint
   */
  async analyzeFood(imageUri: string, mimeType: string = "image/jpeg"): Promise<FoodAnalysisResponse> {
    const formData = new FormData();

    if (Platform.OS === "web") {
      // In web environment, convert URI/blob to File
      const response = await fetch(imageUri);
      const blob = await response.blob();
      formData.append("file", blob, "food_photo.jpg");
    } else {
      // In React Native native environment
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
      timeout: 45000,
    });

    return response.data;
  },

  async createMeal(payload: MealCreatePayload): Promise<Meal> {
    const response = await apiClient.post<Meal>("/meals", payload);
    return response.data;
  },

  async getTodayMeals(): Promise<Meal[]> {
    const response = await apiClient.get<Meal[]>("/meals/today");
    return response.data;
  },

  async getMealsByDate(dateStr: string): Promise<Meal[]> {
    const response = await apiClient.get<Meal[]>(`/meals?date=${dateStr}`);
    return response.data;
  },

  async getMealById(id: number): Promise<Meal> {
    const response = await apiClient.get<Meal>(`/meals/${id}`);
    return response.data;
  },

  async updateMeal(id: number, payload: Partial<MealCreatePayload>): Promise<Meal> {
    const response = await apiClient.put<Meal>(`/meals/${id}`, payload);
    return response.data;
  },

  async deleteMeal(id: number): Promise<void> {
    await apiClient.delete(`/meals/${id}`);
  }
};
