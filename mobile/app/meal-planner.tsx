import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useAuth } from "../hooks/useAuth";
import { useTheme } from "../hooks/useTheme";
import { foodService } from "../services/foodService";
import { MealType } from "../types/food";

interface PlannedMeal {
  type: MealType;
  name: string;
  calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
  prepTime: string;
  ingredients: string[];
  instructions: string;
}

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

const SAMPLE_PLANS: Record<string, PlannedMeal[]> = {
  Mon: [
    {
      type: "Breakfast",
      name: "Greek Yogurt Berry Protein Bowl",
      calories: 360,
      protein_g: 32,
      carbs_g: 38,
      fat_g: 8,
      prepTime: "5 mins",
      ingredients: ["200g Greek Yogurt 0%", "50g Blueberries", "30g Chia Seeds", "1 scoop Whey Protein"],
      instructions: "Mix protein into yogurt until smooth. Top with fresh berries and chia seeds.",
    },
    {
      type: "Lunch",
      name: "Grilled Chicken & Quinoa Harvest Bowl",
      calories: 520,
      protein_g: 48,
      carbs_g: 52,
      fat_g: 12,
      prepTime: "20 mins",
      ingredients: ["180g Chicken Breast", "120g Cooked Quinoa", "80g Baby Spinach", "1 tbsp Olive Oil"],
      instructions: "Pan sear seasoned chicken breast. Toss with warm quinoa, fresh spinach, and light dressing.",
    },
    {
      type: "Snack",
      name: "Apple Slices & Natural Almond Butter",
      calories: 220,
      protein_g: 6,
      carbs_g: 24,
      fat_g: 14,
      prepTime: "3 mins",
      ingredients: ["1 Medium Honeycrisp Apple", "20g Raw Almond Butter"],
      instructions: "Slice apple thinly and serve with natural unsweetened almond butter.",
    },
    {
      type: "Dinner",
      name: "Wild Salmon with Roasted Asparagus & Sweet Potato",
      calories: 580,
      protein_g: 44,
      carbs_g: 42,
      fat_g: 22,
      prepTime: "25 mins",
      ingredients: ["170g Atlantic Salmon Fillet", "150g Roasted Sweet Potato", "100g Asparagus Spears", "Lemon & Herbs"],
      instructions: "Bake salmon at 400°F (200°C) with asparagus and diced sweet potatoes for 18 minutes.",
    },
  ],
  Tue: [
    {
      type: "Breakfast",
      name: "Spinach, Feta & Egg White Scramble",
      calories: 340,
      protein_g: 34,
      carbs_g: 14,
      fat_g: 16,
      prepTime: "10 mins",
      ingredients: ["2 Whole Eggs + 3 Whites", "60g Baby Spinach", "30g Crumbled Feta", "1 slice Whole Grain Toast"],
      instructions: "Scramble eggs with wilted spinach, fold in feta cheese, and serve with toasted whole grain bread.",
    },
    {
      type: "Lunch",
      name: "Lean Grass-Fed Beef & Jasmine Rice Bowl",
      calories: 560,
      protein_g: 50,
      carbs_g: 55,
      fat_g: 14,
      prepTime: "15 mins",
      ingredients: ["170g Lean Ground Beef 93/7", "150g Steamed Jasmine Rice", "80g Bell Peppers", "Coconut Aminos"],
      instructions: "Brown beef with diced peppers and seasonings. Serve atop warm steamed jasmine rice.",
    },
    {
      type: "Snack",
      name: "Cottage Cheese & Crushed Walnut Medley",
      calories: 210,
      protein_g: 22,
      carbs_g: 8,
      fat_g: 10,
      prepTime: "2 mins",
      ingredients: ["180g Low-Fat Cottage Cheese", "15g Raw Walnuts", "Dash of Cinnamon"],
      instructions: "Spoon cottage cheese into bowl, top with crushed walnuts and aromatic cinnamon.",
    },
    {
      type: "Dinner",
      name: "Lemon Herb Baked Cod with Mediterrenean Couscous",
      calories: 490,
      protein_g: 42,
      carbs_g: 48,
      fat_g: 12,
      prepTime: "20 mins",
      ingredients: ["200g Fresh Pacific Cod", "120g Pearl Couscous", "60g Cherry Tomatoes", "Fresh Oregano"],
      instructions: "Bake seasoned cod in parchment with cherry tomatoes and fresh herbs. Serve over couscous.",
    },
  ],
};

export default function MealPlannerScreen() {
  const { user } = useAuth();
  const { colors } = useTheme();
  const router = useRouter();

  const [selectedDay, setSelectedDay] = useState("Mon");
  const [isLogging, setIsLogging] = useState(false);

  const plan = SAMPLE_PLANS[selectedDay] || SAMPLE_PLANS["Mon"];

  const dayTotalCals = plan.reduce((sum, m) => sum + m.calories, 0);
  const dayTotalP = plan.reduce((sum, m) => sum + m.protein_g, 0);
  const dayTotalC = plan.reduce((sum, m) => sum + m.carbs_g, 0);
  const dayTotalF = plan.reduce((sum, m) => sum + m.fat_g, 0);

  const handleLogDayPlan = async () => {
    try {
      setIsLogging(true);
      for (const meal of plan) {
        await foodService.createMeal({
          meal_type: meal.type,
          food_items: [
            {
              name: meal.name,
              estimated_weight_g: 250,
              servings: 1,
              calories: meal.calories,
              protein_g: meal.protein_g,
              carbs_g: meal.carbs_g,
              fat_g: meal.fat_g,
              fiber_g: 4,
              sugar_g: 2,
              sodium_mg: 350,
              confidence: 0.98,
            },
          ],
          notes: `Logged from AI Pro Meal Planner (${selectedDay})`,
        });
      }

      Alert.alert(
        "Meal Plan Logged!",
        `All 4 meals for ${selectedDay} (${dayTotalCals} kcal) have been recorded to your daily food diary.`,
        [
          {
            text: "View Dashboard",
            onPress: () => router.replace("/(tabs)"),
          },
          { text: "Stay Here", style: "cancel" },
        ]
      );
    } catch {
      Alert.alert("Error", "Could not log meal plan.");
    } finally {
      setIsLogging(false);
    }
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      <View style={[styles.header, { borderBottomColor: colors.border }]}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()} activeOpacity={0.7}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <Text style={[styles.headerTitle, { color: colors.text }]}>AI Meal Planner</Text>
        <View style={[styles.vipPill, { backgroundColor: `${colors.amber}20` }]}>
          <Ionicons name="star" size={12} color={colors.amber} />
          <Text style={[styles.vipPillText, { color: colors.amber }]}>PRO</Text>
        </View>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <View style={styles.daySelectorRow}>
          {DAYS.map((day) => {
            const isSelected = selectedDay === day;
            return (
              <TouchableOpacity
                key={day}
                style={[
                  styles.dayChip,
                  {
                    backgroundColor: isSelected ? colors.primary : colors.surfaceHighlight,
                    borderColor: isSelected ? colors.primary : colors.border,
                  },
                ]}
                onPress={() => setSelectedDay(day)}
                activeOpacity={0.7}
              >
                <Text style={[styles.dayChipText, { color: isSelected ? "#FFFFFF" : colors.text }]}>
                  {day}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>

        <View style={[styles.summaryCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Text style={[styles.summaryTitle, { color: colors.text }]}>
            {selectedDay} Nutrition Target Overview
          </Text>
          <View style={styles.macroStrip}>
            <View style={styles.macroItem}>
              <Text style={[styles.macroValue, { color: colors.primary }]}>{dayTotalCals}</Text>
              <Text style={[styles.macroLabel, { color: colors.textSecondary }]}>Total Cals</Text>
            </View>
            <View style={styles.macroItem}>
              <Text style={[styles.macroValue, { color: colors.indigo }]}>{dayTotalP}g</Text>
              <Text style={[styles.macroLabel, { color: colors.textSecondary }]}>Protein</Text>
            </View>
            <View style={styles.macroItem}>
              <Text style={[styles.macroValue, { color: colors.amber }]}>{dayTotalC}g</Text>
              <Text style={[styles.macroLabel, { color: colors.textSecondary }]}>Carbs</Text>
            </View>
            <View style={styles.macroItem}>
              <Text style={[styles.macroValue, { color: colors.rose }]}>{dayTotalF}g</Text>
              <Text style={[styles.macroLabel, { color: colors.textSecondary }]}>Fat</Text>
            </View>
          </View>
        </View>

        <View style={styles.mealsList}>
          {plan.map((meal, index) => (
            <View
              key={index}
              style={[styles.mealCard, { backgroundColor: colors.surface, borderColor: colors.border }]}
            >
              <View style={styles.mealCardHeader}>
                <View style={[styles.typeBadge, { backgroundColor: `${colors.primary}15` }]}>
                  <Text style={[styles.typeBadgeText, { color: colors.primary }]}>{meal.type}</Text>
                </View>
                <View style={styles.prepTimeBox}>
                  <Ionicons name="time-outline" size={13} color={colors.textMuted} />
                  <Text style={[styles.prepTimeText, { color: colors.textMuted }]}>{meal.prepTime}</Text>
                </View>
              </View>

              <Text style={[styles.mealName, { color: colors.text }]}>{meal.name}</Text>

              <View style={styles.miniMacroRow}>
                <Text style={[styles.miniMacro, { color: colors.textSecondary }]}>
                  <Text style={{ fontWeight: "700", color: colors.text }}>{meal.calories}</Text> kcal •{" "}
                  <Text style={{ fontWeight: "700", color: colors.indigo }}>{meal.protein_g}g P</Text> •{" "}
                  <Text style={{ fontWeight: "700", color: colors.amber }}>{meal.carbs_g}g C</Text> •{" "}
                  <Text style={{ fontWeight: "700", color: colors.rose }}>{meal.fat_g}g F</Text>
                </Text>
              </View>

              <View style={[styles.divider, { backgroundColor: colors.border }]} />

              <Text style={[styles.subHeading, { color: colors.textSecondary }]}>INGREDIENTS</Text>
              <View style={styles.ingredientsWrap}>
                {meal.ingredients.map((ing, i) => (
                  <View key={i} style={[styles.ingredientPill, { backgroundColor: colors.surfaceHighlight }]}>
                    <Text style={[styles.ingredientText, { color: colors.text }]}>{ing}</Text>
                  </View>
                ))}
              </View>

              <Text style={[styles.subHeading, { color: colors.textSecondary, marginTop: 10 }]}>PREPARATION</Text>
              <Text style={[styles.instructionsText, { color: colors.textSecondary }]}>
                {meal.instructions}
              </Text>
            </View>
          ))}
        </View>

        <TouchableOpacity
          style={[styles.logDayBtn, { backgroundColor: colors.primary }]}
          onPress={handleLogDayPlan}
          disabled={isLogging}
          activeOpacity={0.8}
        >
          {isLogging ? (
            <ActivityIndicator color="#FFFFFF" />
          ) : (
            <>
              <Ionicons name="add-circle" size={20} color="#FFFFFF" />
              <Text style={styles.logDayBtnText}>Log {selectedDay} Plan to Today's Diary</Text>
            </>
          )}
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  backBtn: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: "800",
  },
  vipPill: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  vipPillText: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.5,
  },
  scrollContent: {
    padding: 16,
    gap: 16,
    paddingBottom: 40,
  },
  daySelectorRow: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  dayChip: {
    flex: 1,
    alignItems: "center",
    paddingVertical: 10,
    marginHorizontal: 3,
    borderRadius: 12,
    borderWidth: 1,
  },
  dayChipText: {
    fontSize: 13,
    fontWeight: "700",
  },
  summaryCard: {
    borderRadius: 18,
    borderWidth: 1,
    padding: 16,
  },
  summaryTitle: {
    fontSize: 14,
    fontWeight: "700",
    marginBottom: 12,
  },
  macroStrip: {
    flexDirection: "row",
    justifyContent: "space-around",
  },
  macroItem: {
    alignItems: "center",
  },
  macroValue: {
    fontSize: 18,
    fontWeight: "800",
    marginBottom: 2,
  },
  macroLabel: {
    fontSize: 11,
    fontWeight: "600",
  },
  mealsList: {
    gap: 14,
  },
  mealCard: {
    borderRadius: 18,
    borderWidth: 1,
    padding: 16,
  },
  mealCardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  typeBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  typeBadgeText: {
    fontSize: 12,
    fontWeight: "800",
  },
  prepTimeBox: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
  },
  prepTimeText: {
    fontSize: 12,
  },
  mealName: {
    fontSize: 16,
    fontWeight: "800",
    marginBottom: 6,
  },
  miniMacroRow: {
    marginBottom: 12,
  },
  miniMacro: {
    fontSize: 13,
  },
  divider: {
    height: 1,
    marginBottom: 12,
  },
  subHeading: {
    fontSize: 10,
    fontWeight: "800",
    letterSpacing: 0.5,
    marginBottom: 6,
  },
  ingredientsWrap: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
    marginBottom: 6,
  },
  ingredientPill: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  ingredientText: {
    fontSize: 12,
  },
  instructionsText: {
    fontSize: 12,
    lineHeight: 18,
  },
  logDayBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    height: 52,
    borderRadius: 14,
    marginTop: 8,
  },
  logDayBtnText: {
    color: "#FFFFFF",
    fontSize: 15,
    fontWeight: "700",
  },
});
