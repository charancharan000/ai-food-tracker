import { FoodItemDetection, NutritionTotal } from "../types/food";

export interface PortionPreset {
  label: "Small" | "Medium" | "Large";
  multiplier: number;
}

export const PORTION_PRESETS: PortionPreset[] = [
  { label: "Small", multiplier: 0.75 },
  { label: "Medium", multiplier: 1.0 },
  { label: "Large", multiplier: 1.5 },
];

/**
 * Recalculate nutritional values proportionally when grams or servings change.
 * Formula: new_val = original_val * (new_weight / original_weight)
 */
export function scaleFoodItemNutrition(
  originalItem: FoodItemDetection,
  newWeightGrams: number,
  newServings: number = 1.0
): FoodItemDetection {
  const baseWeight = originalItem.estimated_weight_g || 100;
  const weightRatio = baseWeight > 0 ? Math.max(0, newWeightGrams / baseWeight) : 1;
  const servingsRatio = (originalItem.servings || 1) > 0 ? Math.max(0, newServings / (originalItem.servings || 1)) : 1;
  
  const totalRatio = weightRatio * servingsRatio;

  return {
    ...originalItem,
    estimated_weight_g: Math.round(newWeightGrams),
    servings: Number(newServings.toFixed(1)),
    calories: Math.round(originalItem.calories * totalRatio * 10) / 10,
    protein_g: Math.round(originalItem.protein_g * totalRatio * 10) / 10,
    carbs_g: Math.round(originalItem.carbs_g * totalRatio * 10) / 10,
    fat_g: Math.round(originalItem.fat_g * totalRatio * 10) / 10,
    fiber_g: Math.round(originalItem.fiber_g * totalRatio * 10) / 10,
    sugar_g: Math.round(originalItem.sugar_g * totalRatio * 10) / 10,
    sodium_mg: Math.round(originalItem.sodium_mg * totalRatio * 10) / 10,
  };
}

/**
 * Calculates sum of all food items in a meal
 */
export function calculateTotals(items: FoodItemDetection[]): NutritionTotal {
  const total: NutritionTotal = {
    calories: 0,
    protein_g: 0,
    carbs_g: 0,
    fat_g: 0,
    fiber_g: 0,
    sugar_g: 0,
    sodium_mg: 0,
  };

  items.forEach((item) => {
    total.calories += item.calories || 0;
    total.protein_g += item.protein_g || 0;
    total.carbs_g += item.carbs_g || 0;
    total.fat_g += item.fat_g || 0;
    total.fiber_g += item.fiber_g || 0;
    total.sugar_g += item.sugar_g || 0;
    total.sodium_mg += item.sodium_mg || 0;
  });

  return {
    calories: Math.round(total.calories * 10) / 10,
    protein_g: Math.round(total.protein_g * 10) / 10,
    carbs_g: Math.round(total.carbs_g * 10) / 10,
    fat_g: Math.round(total.fat_g * 10) / 10,
    fiber_g: Math.round(total.fiber_g * 10) / 10,
    sugar_g: Math.round(total.sugar_g * 10) / 10,
    sodium_mg: Math.round(total.sodium_mg * 10) / 10,
  };
}

/**
 * Estimates BMR and TDEE using the Mifflin-St Jeor formula
 */
export function estimateCalorieTargets(
  age: number = 28,
  gender: string = "male",
  height_cm: number = 175,
  weight_kg: number = 70,
  activity_level: string = "moderate",
  goal: string = "maintain"
) {
  let bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age;
  if (gender.toLowerCase() === "male") {
    bmr += 5;
  } else if (gender.toLowerCase() === "female") {
    bmr -= 161;
  } else {
    bmr -= 78;
  }

  const multipliers: Record<string, number> = {
    sedentary: 1.2,
    light: 1.375,
    moderate: 1.55,
    active: 1.725,
    very_active: 1.9,
  };
  const tdee = bmr * (multipliers[activity_level.toLowerCase()] || 1.55);

  let target = tdee;
  if (goal === "lose") target -= 500;
  if (goal === "gain") target += 400;

  const targetCals = Math.max(1200, Math.round(target));
  const protein = Math.round(Math.min(weight_kg * 2.0, (targetCals * 0.3) / 4));
  const fat = Math.round((targetCals * 0.25) / 9);
  const carbs = Math.max(50, Math.round((targetCals - (protein * 4 + fat * 9)) / 4));
  const water = Math.round((weight_kg * 35) / 250) * 250;

  return {
    calories: targetCals,
    protein,
    carbs,
    fat,
    water: Math.max(2000, water),
  };
}
