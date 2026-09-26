import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../hooks/useTheme";
import { Meal, MealType } from "../types/food";

interface MealCardProps {
  mealType: MealType;
  calories: number;
  meals: Meal[];
  onAddPress: () => void;
  onMealPress?: (meal: Meal) => void;
}

export const MealCard: React.FC<MealCardProps> = React.memo(({
  mealType,
  calories,
  meals,
  onAddPress,
  onMealPress,
}) => {
  const { colors } = useTheme();

  const getMealIcon = (type: MealType): keyof typeof Ionicons.glyphMap => {
    switch (type) {
      case "Breakfast":
        return "sunny-outline";
      case "Lunch":
        return "restaurant-outline";
      case "Snack":
        return "nutrition-outline";
      case "Dinner":
        return "moon-outline";
      default:
        return "fast-food-outline";
    }
  };

  const getMealColor = (type: MealType) => {
    switch (type) {
      case "Breakfast":
        return colors.amber;
      case "Lunch":
        return colors.emerald;
      case "Snack":
        return colors.cyan;
      case "Dinner":
        return colors.primary;
      default:
        return colors.primary;
    }
  };

  const iconColor = getMealColor(mealType);

  return (
    <View
      style={[
        styles.card,
        {
          backgroundColor: colors.surface,
          borderColor: colors.border,
        },
      ]}
    >
      <View style={styles.headerRow}>
        <View style={styles.titleGroup}>
          <View style={[styles.iconBox, { backgroundColor: `${iconColor}18` }]}>
            <Ionicons name={getMealIcon(mealType)} size={20} color={iconColor} />
          </View>
          <View>
            <Text style={[styles.mealTitle, { color: colors.text }]}>{mealType}</Text>
            <Text style={[styles.calorieCount, { color: colors.textSecondary }]}>
              {Math.round(calories)} kcal
            </Text>
          </View>
        </View>

        <TouchableOpacity
          style={[styles.addButton, { backgroundColor: colors.surfaceHighlight }]}
          onPress={onAddPress}
          activeOpacity={0.7}
        >
          <Ionicons name="add" size={20} color={colors.primary} />
        </TouchableOpacity>
      </View>

      {meals.length > 0 ? (
        <View style={styles.mealList}>
          {meals.map((meal) => (
            <TouchableOpacity
              key={meal.id}
              style={[styles.mealItemRow, { borderTopColor: colors.surfaceHighlight }]}
              onPress={() => onMealPress && onMealPress(meal)}
              activeOpacity={0.7}
            >
              <View style={styles.mealDetails}>
                <Text style={[styles.mealNames, { color: colors.text }]} numberOfLines={1}>
                  {meal.food_items.map((i) => i.name).join(", ")}
                </Text>
                <View style={styles.macroBadges}>
                  <View style={[styles.macroPillBox, { backgroundColor: `${colors.emerald}15` }]}>
                    <Text style={[styles.macroPill, { color: colors.emerald }]}>
                      {Math.round(meal.total_calories)} kcal
                    </Text>
                  </View>
                  <View style={[styles.macroPillBox, { backgroundColor: `${colors.indigo}15` }]}>
                    <Text style={[styles.macroPill, { color: colors.indigo }]}>
                      P: {Math.round(meal.total_protein)}g
                    </Text>
                  </View>
                  <View style={[styles.macroPillBox, { backgroundColor: `${colors.amber}15` }]}>
                    <Text style={[styles.macroPill, { color: colors.amber }]}>
                      C: {Math.round(meal.total_carbs)}g
                    </Text>
                  </View>
                  <View style={[styles.macroPillBox, { backgroundColor: `${colors.rose}15` }]}>
                    <Text style={[styles.macroPill, { color: colors.rose }]}>
                      F: {Math.round(meal.total_fat)}g
                    </Text>
                  </View>
                </View>
              </View>
              <Ionicons name="chevron-forward" size={16} color={colors.textMuted} />
            </TouchableOpacity>
          ))}
        </View>
      ) : (
        <Text style={[styles.emptyPrompt, { color: colors.textMuted }]}>
          No meals logged yet. Tap + to scan or log.
        </Text>
      )}
    </View>
  );
});

const styles = StyleSheet.create({
  card: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 16,
    marginBottom: 14,
  },
  headerRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  titleGroup: {
    flexDirection: "row",
    alignItems: "center",
  },
  iconBox: {
    width: 40,
    height: 40,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 12,
  },
  mealTitle: {
    fontSize: 16,
    fontWeight: "800",
    letterSpacing: -0.2,
  },
  calorieCount: {
    fontSize: 13,
    fontWeight: "600",
    marginTop: 1,
  },
  addButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: "center",
    justifyContent: "center",
  },
  emptyPrompt: {
    fontSize: 12,
    fontWeight: "500",
    fontStyle: "italic",
    marginTop: 10,
    opacity: 0.8,
  },
  mealList: {
    marginTop: 12,
  },
  mealItemRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingVertical: 10,
    borderTopWidth: 1,
  },
  mealDetails: {
    flex: 1,
    marginRight: 10,
  },
  mealNames: {
    fontSize: 14,
    fontWeight: "700",
    marginBottom: 6,
  },
  macroBadges: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 6,
  },
  macroPillBox: {
    paddingHorizontal: 7,
    paddingVertical: 2,
    borderRadius: 6,
  },
  macroPill: {
    fontSize: 11,
    fontWeight: "700",
  },
});
