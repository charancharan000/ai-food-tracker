export interface FoodItemDetection {
  id?: number;
  name: string;
  estimated_weight_g: number;
  servings: number;
  calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
  fiber_g: number;
  sugar_g: number;
  sodium_mg: number;
  confidence: number;
}

export interface NutritionTotal {
  calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
  fiber_g: number;
  sugar_g: number;
  sodium_mg: number;
}

export interface FoodAnalysisResponse {
  food_items: FoodItemDetection[];
  total: NutritionTotal;
  notes: string;
  image_preview_url?: string;
}

export type MealType = "Breakfast" | "Lunch" | "Snack" | "Dinner";

export interface Meal {
  id: number;
  user_id: number;
  meal_type: MealType;
  meal_date: string;
  total_calories: number;
  total_protein: number;
  total_carbs: number;
  total_fat: number;
  total_fiber: number;
  total_sugar: number;
  total_sodium: number;
  image_url?: string | null;
  notes?: string | null;
  created_at: string;
  food_items: FoodItemDetection[];
}

export interface MealCreatePayload {
  meal_type: MealType;
  meal_date?: string;
  notes?: string;
  image_url?: string;
  food_items: {
    name: string;
    estimated_weight_g: number;
    servings: number;
    calories: number;
    protein_g: number;
    carbs_g: number;
    fat_g: number;
    fiber_g: number;
    sugar_g: number;
    sodium_mg: number;
    confidence: number;
  }[];
}
