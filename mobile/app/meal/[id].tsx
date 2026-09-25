import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../../hooks/useTheme";
import { foodService } from "../../services/foodService";
import { Meal, FoodItemDetection } from "../../types/food";
import { FoodItemCard } from "../../components/FoodItemCard";
import { NutritionSummaryBar } from "../../components/NutritionSummaryBar";
import { calculateTotals } from "../../utils/nutrition";
import { formatDateLabel, formatTime } from "../../utils/formatters";

export default function MealDetailsScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { colors } = useTheme();

  const [meal, setMeal] = useState<Meal | null>(null);
  const [items, setItems] = useState<FoodItemDetection[]>([]);
  const [originalItems, setOriginalItems] = useState<FoodItemDetection[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (id) {
      loadMeal(parseInt(id, 10));
    }
  }, [id]);

  const loadMeal = async (mealId: number) => {
    try {
      setLoading(true);
      const data = await foodService.getMealById(mealId);
      setMeal(data);
      setItems(data.food_items);
      setOriginalItems(JSON.parse(JSON.stringify(data.food_items)));
    } catch {
      Alert.alert("Error", "Could not load meal details.");
      router.back();
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateItem = (index: number, updated: FoodItemDetection) => {
    const next = [...items];
    next[index] = updated;
    setItems(next);
  };

  const handleRemoveItem = (index: number) => {
    if (items.length === 1) {
      Alert.alert("Notice", "Cannot remove the only item from the meal. Delete the meal instead.");
      return;
    }
    const next = items.filter((_, i) => i !== index);
    setItems(next);
  };

  const handleSaveChanges = async () => {
    if (!meal) return;
    try {
      setSaving(true);
      await foodService.updateMeal(meal.id, {
        meal_type: meal.meal_type,
        notes: meal.notes || "",
        food_items: items.map((i) => ({
          name: i.name,
          estimated_weight_g: i.estimated_weight_g,
          servings: i.servings,
          calories: i.calories,
          protein_g: i.protein_g,
          carbs_g: i.carbs_g,
          fat_g: i.fat_g,
          fiber_g: i.fiber_g,
          sugar_g: i.sugar_g,
          sodium_mg: i.sodium_mg,
          confidence: i.confidence,
        })),
      });
      Alert.alert("Success", "Meal changes saved.");
      router.back();
    } catch {
      Alert.alert("Error", "Failed to save meal changes.");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = () => {
    if (!meal) return;
    Alert.alert("Delete Meal", "Are you sure you want to permanently delete this meal?", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Delete",
        style: "destructive",
        onPress: async () => {
          try {
            await foodService.deleteMeal(meal.id);
            router.back();
          } catch {
            Alert.alert("Error", "Could not delete meal.");
          }
        },
      },
    ]);
  };

  if (loading) {
    return (
      <View style={[styles.center, { backgroundColor: colors.background }]}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  if (!meal) return null;

  const totals = calculateTotals(items);

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["bottom"]}>
      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* Header Summary Card */}
        <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <View style={styles.topRow}>
            <View>
              <Text style={[styles.mealTypeBadge, { color: colors.primary }]}>{meal.meal_type}</Text>
              <Text style={[styles.timeLabel, { color: colors.textSecondary }]}>
                {formatDateLabel(meal.meal_date)} at {formatTime(meal.created_at)}
              </Text>
            </View>

            <TouchableOpacity style={styles.trashBtn} onPress={handleDelete}>
              <Ionicons name="trash-outline" size={20} color={colors.danger} />
            </TouchableOpacity>
          </View>

          <NutritionSummaryBar total={totals} />

          {meal.notes ? (
            <Text style={[styles.notesText, { color: colors.textMuted }]}>Notes: {meal.notes}</Text>
          ) : null}
        </View>

        {/* Food Items List */}
        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>
          FOOD ITEMS ({items.length})
        </Text>

        {items.map((item, idx) => (
          <FoodItemCard
            key={`${item.name}-${idx}`}
            item={item}
            originalItem={originalItems[idx] || item}
            index={idx}
            onUpdate={(u) => handleUpdateItem(idx, u)}
            onRemove={() => handleRemoveItem(idx)}
          />
        ))}

        {/* Save Changes Button */}
        <TouchableOpacity
          style={[styles.saveBtn, { backgroundColor: colors.primary }]}
          onPress={handleSaveChanges}
          disabled={saving}
          activeOpacity={0.8}
        >
          {saving ? (
            <ActivityIndicator color="#FFFFFF" />
          ) : (
            <Text style={styles.saveBtnText}>Save Portion Adjustments</Text>
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
  center: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  card: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 18,
    marginBottom: 16,
  },
  topRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  mealTypeBadge: {
    fontSize: 20,
    fontWeight: "800",
  },
  timeLabel: {
    fontSize: 12,
    marginTop: 2,
  },
  trashBtn: {
    padding: 8,
  },
  notesText: {
    fontSize: 12,
    fontStyle: "italic",
    marginTop: 6,
  },
  sectionTitle: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
    marginBottom: 10,
  },
  saveBtn: {
    height: 52,
    borderRadius: 16,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 14,
  },
  saveBtnText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
});
