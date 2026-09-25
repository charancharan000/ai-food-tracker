import { Meal } from "./food";

export interface MacroBreakdown {
  consumed: number;
  target: number;
  remaining: number;
  percentage: number;
}

export interface MealsByType {
  calories: number;
  count: number;
  meals: Meal[];
}

export interface DashboardToday {
  date: string;
  calories_consumed: number;
  daily_calorie_target: number;
  calories_remaining: number;
  calories_percentage: number;
  protein: MacroBreakdown;
  carbs: MacroBreakdown;
  fat: MacroBreakdown;
  water_consumed_ml: number;
  water_target_ml: number;
  water_percentage: number;
  meals_by_type: {
    Breakfast: MealsByType;
    Lunch: MealsByType;
    Snack: MealsByType;
    Dinner: MealsByType;
    [key: string]: MealsByType;
  };
  recent_meals: Meal[];
}

export interface DailySummaryItem {
  date: string;
  calories: number;
  target_calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
  meal_count: number;
}

export interface DashboardSummary {
  timeframe: string;
  start_date: string;
  end_date: string;
  average_daily_calories: number;
  total_calories: number;
  total_meals: number;
  daily_stats: DailySummaryItem[];
}
