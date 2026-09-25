import { apiClient } from "./api";
import { WaterLog, WaterTodayResponse } from "../types/water";

export const waterService = {
  async logWater(amount_ml: number, date?: string): Promise<WaterLog> {
    const response = await apiClient.post<WaterLog>("/water", {
      amount_ml,
      date,
    });
    return response.data;
  },

  async getWaterToday(): Promise<WaterTodayResponse> {
    const response = await apiClient.get<WaterTodayResponse>("/water/today");
    return response.data;
  },

  async deleteWaterLog(id: number): Promise<void> {
    await apiClient.delete(`/water/${id}`);
  }
};
