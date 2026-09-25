import { scaleFoodItemNutrition, calculateTotals, estimateCalorieTargets } from "../utils/nutrition";
import { FoodItemDetection } from "../types/food";

describe("Frontend Nutrition Calculations", () => {
  const sampleItem: FoodItemDetection = {
    name: "Chicken Biryani",
    estimated_weight_g: 300,
    servings: 1.0,
    calories: 600,
    protein_g: 30,
    carbs_g: 75,
    fat_g: 20,
    fiber_g: 4,
    sugar_g: 5,
    sodium_mg: 800,
    confidence: 0.85,
  };

  test("exact proportional scaling when weight changes 300g -> 450g", () => {
    const updated = scaleFoodItemNutrition(sampleItem, 450, 1.0);
    expect(updated.estimated_weight_g).toBe(450);
    expect(updated.calories).toBe(900);
    expect(updated.protein_g).toBe(45);
    expect(updated.carbs_g).toBe(112.5);
    expect(updated.fat_g).toBe(30);
    expect(updated.fiber_g).toBe(6);
    expect(updated.sugar_g).toBe(7.5);
    expect(updated.sodium_mg).toBe(1200);
  });

  test("servings multiplier scaling", () => {
    const updated = scaleFoodItemNutrition(sampleItem, 300, 2.0);
    expect(updated.calories).toBe(1200);
    expect(updated.protein_g).toBe(60);
  });

  test("meal totals summation across multiple foods", () => {
    const items: FoodItemDetection[] = [
      { name: "Rice", estimated_weight_g: 220, servings: 1, calories: 285, protein_g: 5.8, carbs_g: 62, fat_g: 0.6, fiber_g: 1.2, sugar_g: 0.2, sodium_mg: 15, confidence: 0.9 },
      { name: "Chicken Curry", estimated_weight_g: 150, servings: 1, calories: 280, protein_g: 26, carbs_g: 8, fat_g: 16, fiber_g: 2.1, sugar_g: 3, sodium_mg: 620, confidence: 0.9 },
      { name: "Dal", estimated_weight_g: 120, servings: 1, calories: 140, protein_g: 8.5, carbs_g: 20, fat_g: 3.2, fiber_g: 4.5, sugar_g: 1.5, sodium_mg: 450, confidence: 0.85 },
      { name: "Salad", estimated_weight_g: 100, servings: 1, calories: 35, protein_g: 1.5, carbs_g: 7, fat_g: 0.3, fiber_g: 2.5, sugar_g: 3.2, sodium_mg: 25, confidence: 0.8 },
    ];

    const totals = calculateTotals(items);
    expect(totals.calories).toBe(740);
    expect(totals.protein_g).toBe(41.8);
    expect(totals.carbs_g).toBe(97);
    expect(totals.fat_g).toBe(20.1);
  });

  test("estimateCalorieTargets generates realistic targets", () => {
    const targets = estimateCalorieTargets(30, "male", 180, 80, "moderate", "lose");
    expect(targets.calories).toBeGreaterThan(1500);
    expect(targets.protein).toBeGreaterThanOrEqual(140);
    expect(targets.carbs).toBeGreaterThan(50);
    expect(targets.fat).toBeGreaterThan(30);
    expect(targets.water).toBeGreaterThanOrEqual(2500);
  });
});
