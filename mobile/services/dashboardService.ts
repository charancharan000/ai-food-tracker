import { apiClient } from "./api";
import { DashboardToday, DashboardSummary } from "../types/dashboard";

export const dashboardService = {
  async getDashboardToday(): Promise<DashboardToday> {
    const response = await apiClient.get<DashboardToday>("/dashboard/today");
    return response.data;
  },

  async getDashboardSummary(timeframe: "today" | "yesterday" | "week" | "month" = "week"): Promise<DashboardSummary> {
    const response = await apiClient.get<DashboardSummary>(`/dashboard/summary?timeframe=${timeframe}`);
    return response.data;
  }
};
