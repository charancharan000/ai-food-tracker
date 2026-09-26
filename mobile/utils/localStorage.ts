import AsyncStorage from "@react-native-async-storage/async-storage";
import { Meal, MealCreatePayload, FoodAnalysisResponse, MealType } from "../types/food";
import { DashboardToday, DashboardSummary, DailySummaryItem } from "../types/dashboard";
import { User } from "../types/auth";
import { calculateTotals } from "./nutrition";

const LOCAL_MEALS_KEY = "@nutriscan_local_meals";
const LOCAL_WATER_KEY = "@nutriscan_local_water";

export interface LocalWaterEntry {
  id: number;
  amount_ml: number;
  date: string;
  created_at: string;
}

function getTodayDateString(): string {
  return new Date().toISOString().split("T")[0];
}

export const localStore = {
  async getMeals(): Promise<Meal[]> {
    try {
      const data = await AsyncStorage.getItem(LOCAL_MEALS_KEY);
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  },

  async saveMeal(payload: MealCreatePayload, userId: number = 1): Promise<Meal> {
    const meals = await this.getMeals();
    const totals = calculateTotals(payload.food_items as any);
    const mealDate = payload.meal_date || getTodayDateString();

    const newMeal: Meal = {
      id: Date.now(),
      user_id: userId,
      meal_type: payload.meal_type,
      meal_date: mealDate,
      total_calories: totals.calories,
      total_protein: totals.protein_g,
      total_carbs: totals.carbs_g,
      total_fat: totals.fat_g,
      total_fiber: totals.fiber_g,
      total_sugar: totals.sugar_g,
      total_sodium: totals.sodium_mg,
      image_url: payload.image_url || null,
      notes: payload.notes || null,
      created_at: new Date().toISOString(),
      food_items: payload.food_items.map((it, idx) => ({
        ...it,
        id: Date.now() + idx,
      })),
    };

    meals.unshift(newMeal);
    await AsyncStorage.setItem(LOCAL_MEALS_KEY, JSON.stringify(meals));
    return newMeal;
  },

  async getMealsByDate(dateStr: string): Promise<Meal[]> {
    const meals = await this.getMeals();
    return meals.filter((m) => m.meal_date === dateStr);
  },

  async getMealById(id: number): Promise<Meal | null> {
    const meals = await this.getMeals();
    return meals.find((m) => m.id === id) || null;
  },

  async updateMeal(id: number, payload: Partial<MealCreatePayload>): Promise<Meal | null> {
    const meals = await this.getMeals();
    const index = meals.findIndex((m) => m.id === id);
    if (index === -1) return null;

    const existing = meals[index];
    const items = (payload.food_items as any) || existing.food_items;
    const totals = calculateTotals(items);

    const updated: Meal = {
      ...existing,
      meal_type: payload.meal_type || existing.meal_type,
      meal_date: payload.meal_date || existing.meal_date,
      notes: payload.notes !== undefined ? payload.notes : existing.notes,
      total_calories: totals.calories,
      total_protein: totals.protein_g,
      total_carbs: totals.carbs_g,
      total_fat: totals.fat_g,
      total_fiber: totals.fiber_g,
      total_sugar: totals.sugar_g,
      total_sodium: totals.sodium_mg,
      food_items: items,
    };

    meals[index] = updated;
    await AsyncStorage.setItem(LOCAL_MEALS_KEY, JSON.stringify(meals));
    return updated;
  },

  async deleteMeal(id: number): Promise<void> {
    const meals = await this.getMeals();
    const filtered = meals.filter((m) => m.id !== id);
    await AsyncStorage.setItem(LOCAL_MEALS_KEY, JSON.stringify(filtered));
  },

  async getWaterLogs(): Promise<LocalWaterEntry[]> {
    try {
      const data = await AsyncStorage.getItem(LOCAL_WATER_KEY);
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  },

  async addWaterLog(amount_ml: number, dateStr?: string): Promise<LocalWaterEntry> {
    const logs = await this.getWaterLogs();
    const entry: LocalWaterEntry = {
      id: Date.now(),
      amount_ml,
      date: dateStr || getTodayDateString(),
      created_at: new Date().toISOString(),
    };
    logs.unshift(entry);
    await AsyncStorage.setItem(LOCAL_WATER_KEY, JSON.stringify(logs));
    return entry;
  },

  async getTodayWaterMl(dateStr?: string): Promise<number> {
    const targetDate = dateStr || getTodayDateString();
    const logs = await this.getWaterLogs();
    return logs
      .filter((l) => l.date === targetDate)
      .reduce((sum, l) => sum + l.amount_ml, 0);
  },

  async deleteWaterLog(id: number): Promise<void> {
    const logs = await this.getWaterLogs();
    const filtered = logs.filter((l) => l.id !== id);
    await AsyncStorage.setItem(LOCAL_WATER_KEY, JSON.stringify(filtered));
  },

  async getDashboardToday(user: User | null): Promise<DashboardToday> {
    const today = getTodayDateString();
    const todayMeals = await this.getMealsByDate(today);
    const waterConsumed = await this.getTodayWaterMl(today);

    const calorieTarget = user?.daily_calorie_target || 2000;
    const proteinTarget = user?.protein_target || 140;
    const carbTarget = user?.carb_target || 220;
    const fatTarget = user?.fat_target || 65;
    const waterTarget = user?.daily_water_target_ml || 2500;

    let totalCals = 0;
    let totalProtein = 0;
    let totalCarbs = 0;
    let totalFat = 0;

    const mealsByType: Record<MealType, { calories: number; count: number; meals: Meal[] }> = {
      Breakfast: { calories: 0, count: 0, meals: [] },
      Lunch: { calories: 0, count: 0, meals: [] },
      Snack: { calories: 0, count: 0, meals: [] },
      Dinner: { calories: 0, count: 0, meals: [] },
    };

    todayMeals.forEach((meal) => {
      totalCals += meal.total_calories || 0;
      totalProtein += meal.total_protein || 0;
      totalCarbs += meal.total_carbs || 0;
      totalFat += meal.total_fat || 0;

      const type = (meal.meal_type || "Snack") as MealType;
      if (mealsByType[type]) {
        mealsByType[type].calories += meal.total_calories || 0;
        mealsByType[type].count += 1;
        mealsByType[type].meals.push(meal);
      }
    });

    const calsRemaining = Math.max(0, calorieTarget - totalCals);
    const calsPercent = calorieTarget > 0 ? Math.min(100, Math.round((totalCals / calorieTarget) * 100)) : 0;
    const waterPercent = waterTarget > 0 ? Math.min(100, Math.round((waterConsumed / waterTarget) * 100)) : 0;

    return {
      date: today,
      calories_consumed: Math.round(totalCals),
      daily_calorie_target: calorieTarget,
      calories_remaining: Math.round(calsRemaining),
      calories_percentage: calsPercent,
      protein: {
        consumed: Math.round(totalProtein),
        target: proteinTarget,
        remaining: Math.max(0, proteinTarget - Math.round(totalProtein)),
        percentage: proteinTarget > 0 ? Math.min(100, Math.round((totalProtein / proteinTarget) * 100)) : 0,
      },
      carbs: {
        consumed: Math.round(totalCarbs),
        target: carbTarget,
        remaining: Math.max(0, carbTarget - Math.round(totalCarbs)),
        percentage: carbTarget > 0 ? Math.min(100, Math.round((totalCarbs / carbTarget) * 100)) : 0,
      },
      fat: {
        consumed: Math.round(totalFat),
        target: fatTarget,
        remaining: Math.max(0, fatTarget - Math.round(totalFat)),
        percentage: fatTarget > 0 ? Math.min(100, Math.round((totalFat / fatTarget) * 100)) : 0,
      },
      water_consumed_ml: waterConsumed,
      water_target_ml: waterTarget,
      water_percentage: waterPercent,
      meals_by_type: mealsByType,
      recent_meals: todayMeals.slice(0, 5),
    };
  },

  async getDashboardSummary(user: User | null, timeframe: string = "week"): Promise<DashboardSummary> {
    const meals = await this.getMeals();
    const daysCount = timeframe === "today" ? 1 : timeframe === "yesterday" ? 1 : timeframe === "month" ? 30 : 7;
    const today = new Date();
    const dailyStats: DailySummaryItem[] = [];
    const calorieTarget = user?.daily_calorie_target || 2000;

    let totalCals = 0;
    let totalMealsCount = 0;

    for (let i = daysCount - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      const dateStr = d.toISOString().split("T")[0];
      const dayMeals = meals.filter((m) => m.meal_date === dateStr);

      let dayCals = 0;
      let dayP = 0;
      let dayC = 0;
      let dayF = 0;

      dayMeals.forEach((m) => {
        dayCals += m.total_calories || 0;
        dayP += m.total_protein || 0;
        dayC += m.total_carbs || 0;
        dayF += m.total_fat || 0;
      });

      totalCals += dayCals;
      totalMealsCount += dayMeals.length;

      dailyStats.push({
        date: dateStr,
        calories: Math.round(dayCals),
        target_calories: calorieTarget,
        protein_g: Math.round(dayP),
        carbs_g: Math.round(dayC),
        fat_g: Math.round(dayF),
        meal_count: dayMeals.length,
      });
    }

    const avgCals = daysCount > 0 ? Math.round(totalCals / daysCount) : 0;
    const startDate = dailyStats.length > 0 ? dailyStats[0].date : getTodayDateString();
    const endDate = dailyStats.length > 0 ? dailyStats[dailyStats.length - 1].date : getTodayDateString();

    return {
      timeframe,
      start_date: startDate,
      end_date: endDate,
      average_daily_calories: avgCals,
      total_calories: Math.round(totalCals),
      total_meals: totalMealsCount,
      daily_stats: dailyStats,
    };
  },

  getMockAnalysis(): FoodAnalysisResponse {
    const presets: FoodAnalysisResponse[] = [
      {
        food_items: [
          {
            name: "Grilled Chicken Breast",
            estimated_weight_g: 150,
            servings: 1,
            calories: 247,
            protein_g: 46.5,
            carbs_g: 0,
            fat_g: 5.4,
            fiber_g: 0,
            sugar_g: 0,
            sodium_mg: 380,
            confidence: 0.96,
          },
          {
            name: "Brown Rice",
            estimated_weight_g: 150,
            servings: 1,
            calories: 168,
            protein_g: 3.8,
            carbs_g: 35.2,
            fat_g: 1.4,
            fiber_g: 2.4,
            sugar_g: 0.4,
            sodium_mg: 5,
            confidence: 0.92,
          },
          {
            name: "Steamed Broccoli",
            estimated_weight_g: 100,
            servings: 1,
            calories: 35,
            protein_g: 2.4,
            carbs_g: 7.2,
            fat_g: 0.4,
            fiber_g: 2.6,
            sugar_g: 1.4,
            sodium_mg: 33,
            confidence: 0.94,
          },
        ],
        total: {
          calories: 450,
          protein_g: 52.7,
          carbs_g: 42.4,
          fat_g: 7.2,
          fiber_g: 5.0,
          sugar_g: 1.8,
          sodium_mg: 418,
        },
        notes: "Balanced high-protein fitness meal with complex carbohydrates and greens.",
      },
      {
        food_items: [
          {
            name: "Avocado Toast",
            estimated_weight_g: 140,
            servings: 1,
            calories: 280,
            protein_g: 6.5,
            carbs_g: 26.0,
            fat_g: 17.5,
            fiber_g: 7.2,
            sugar_g: 1.8,
            sodium_mg: 290,
            confidence: 0.95,
          },
          {
            name: "Poached Egg",
            estimated_weight_g: 50,
            servings: 1,
            calories: 72,
            protein_g: 6.3,
            carbs_g: 0.4,
            fat_g: 4.8,
            fiber_g: 0,
            sugar_g: 0.2,
            sodium_mg: 142,
            confidence: 0.97,
          },
        ],
        total: {
          calories: 352,
          protein_g: 12.8,
          carbs_g: 26.4,
          fat_g: 22.3,
          fiber_g: 7.2,
          sugar_g: 2.0,
          sodium_mg: 432,
        },
        notes: "Nutrient-dense breakfast rich in healthy monounsaturated fats and micronutrients.",
      },
    ];

    const idx = Math.floor(Math.random() * presets.length);
    return presets[idx];
  },
};
