import { apiClient } from "./api";
import { WaterLog, WaterTodayResponse } from "../types/water";
import { localStore } from "../utils/localStorage";
import { storage } from "../utils/storage";

export const waterService = {
  async logWater(amount_ml: number, date?: string): Promise<WaterLog> {
    try {
      const response = await apiClient.post<WaterLog>("/water", {
        amount_ml,
        date,
      });
      return response.data;
    } catch {
      const entry = await localStore.addWaterLog(amount_ml, date);
      return {
        id: entry.id,
        user_id: 1,
        amount_ml: entry.amount_ml,
        date: entry.date,
        created_at: entry.created_at,
      };
    }
  },

  async getWaterToday(): Promise<WaterTodayResponse> {
    try {
      const response = await apiClient.get<WaterTodayResponse>("/water/today");
      return response.data;
    } catch {
      const user = await storage.getUser();
      const target = user?.daily_water_target_ml || 2500;
      const consumed = await localStore.getTodayWaterMl();
      const percent = target > 0 ? Math.min(100, Math.round((consumed / target) * 100)) : 0;
      const remaining = Math.max(0, target - consumed);

      return {
        date: new Date().toISOString().split("T")[0],
        total_ml: consumed,
        target_ml: target,
        percentage: percent,
        remaining_ml: remaining,
        logs: [],
      };
    }
  },

  async deleteWaterLog(id: number): Promise<void> {
    try {
      await apiClient.delete(`/water/${id}`);
    } catch {
      await localStore.deleteWaterLog(id);
    }
  }
};
