export interface WaterLog {
  id: number;
  user_id: number;
  date: string;
  amount_ml: number;
  created_at: string;
}

export interface WaterTodayResponse {
  date: string;
  total_ml: number;
  target_ml: number;
  remaining_ml: number;
  percentage: number;
  logs: WaterLog[];
}
