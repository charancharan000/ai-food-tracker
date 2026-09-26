import { apiClient } from "./api";
import { DashboardToday, DashboardSummary } from "../types/dashboard";
import { localStore } from "../utils/localStorage";
import { storage } from "../utils/storage";

export const dashboardService = {
  async getDashboardToday(): Promise<DashboardToday> {
    try {
      const response = await apiClient.get<DashboardToday>("/dashboard/today");
      return response.data;
    } catch {
      const user = await storage.getUser();
      return await localStore.getDashboardToday(user);
    }
  },

  async getDashboardSummary(timeframe: "today" | "yesterday" | "week" | "month" = "week"): Promise<DashboardSummary> {
    try {
      const response = await apiClient.get<DashboardSummary>(`/dashboard/summary?timeframe=${timeframe}`);
      return response.data;
    } catch {
      const user = await storage.getUser();
      return await localStore.getDashboardSummary(user, timeframe);
    }
  }
};
