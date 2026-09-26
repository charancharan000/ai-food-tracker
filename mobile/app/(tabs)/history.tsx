import React, { useState, useEffect, useCallback } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  Alert,
  ActivityIndicator,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../../hooks/useTheme";
import { foodService } from "../../services/foodService";
import { dashboardService } from "../../services/dashboardService";
import { Meal, MealType } from "../../types/food";
import { DashboardSummary } from "../../types/dashboard";
import { formatDateLabel, formatTime } from "../../utils/formatters";
import { Skeleton } from "../../components/SkeletonLoader";

export default function HistoryScreen() {
  const { colors } = useTheme();
  const router = useRouter();

  const [activeTab, setActiveTab] = useState<"log" | "charts">("log");
  const [timeframe, setTimeframe] = useState<"today" | "yesterday" | "week" | "month">("today");
  const [meals, setMeals] = useState<Meal[]>([]);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = useCallback(async () => {
    try {
      if (activeTab === "log") {
        let dateQuery: string | undefined;
        const now = new Date();
        if (timeframe === "today") {
          dateQuery = now.toISOString().split("T")[0];
        } else if (timeframe === "yesterday") {
          const y = new Date();
          y.setDate(y.getDate() - 1);
          dateQuery = y.toISOString().split("T")[0];
        }
        const data = await foodService.getMealsByDate(dateQuery || "");
        setMeals(data);
      } else {
        const sumData = await dashboardService.getDashboardSummary(timeframe);
        setSummary(sumData);
      }
    } catch (e) {
      console.error("Error loading history", e);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [activeTab, timeframe]);

  useEffect(() => {
    setLoading(true);
    loadData();
  }, [loadData]);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const handleDeleteMeal = (mealId: number) => {
    Alert.alert(
      "Delete Meal",
      "Are you sure you want to remove this meal from your log?",
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Delete",
          style: "destructive",
          onPress: async () => {
            try {
              await foodService.deleteMeal(mealId);
              setMeals(meals.filter((m) => m.id !== mealId));
            } catch {
              Alert.alert("Error", "Could not delete meal.");
            }
          },
        },
      ]
    );
  };

  const handleDuplicateMeal = async (meal: Meal) => {
    try {
      await foodService.createMeal({
        meal_type: meal.meal_type,
        notes: `Duplicated from ${meal.meal_type}`,
        food_items: meal.food_items.map((i) => ({
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
      Alert.alert("Success", "Meal duplicated into today's log.");
      loadData();
    } catch {
      Alert.alert("Error", "Failed to duplicate meal.");
    }
  };

  const mealTypes: MealType[] = ["Breakfast", "Lunch", "Snack", "Dinner"];

  const totalCalories = meals.reduce((acc, m) => acc + m.total_calories, 0);
  const totalProtein = meals.reduce((acc, m) => acc + m.total_protein, 0);
  const totalCarbs = meals.reduce((acc, m) => acc + m.total_carbs, 0);
  const totalFat = meals.reduce((acc, m) => acc + m.total_fat, 0);

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      <View style={styles.topBar}>
        <Text style={[styles.headerTitle, { color: colors.text }]}>Food Log</Text>
        
        <View style={[styles.tabSwitch, { backgroundColor: colors.surfaceHighlight }]}>
          <TouchableOpacity
            style={[
              styles.switchBtn,
              activeTab === "log" && { backgroundColor: colors.primary },
            ]}
            onPress={() => setActiveTab("log")}
          >
            <Text
              style={[
                styles.switchBtnText,
                { color: activeTab === "log" ? "#FFFFFF" : colors.textSecondary },
              ]}
            >
              Log
            </Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.switchBtn,
              activeTab === "charts" && { backgroundColor: colors.primary },
            ]}
            onPress={() => setActiveTab("charts")}
          >
            <Text
              style={[
                styles.switchBtnText,
                { color: activeTab === "charts" ? "#FFFFFF" : colors.textSecondary },
              ]}
            >
              Charts
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.timeframeRow}>
        {(["today", "yesterday", "week", "month"] as const).map((tf) => (
          <TouchableOpacity
            key={tf}
            style={[
              styles.timeframeChip,
              {
                backgroundColor: timeframe === tf ? colors.primary : colors.surface,
                borderColor: timeframe === tf ? colors.primary : colors.border,
              },
            ]}
            onPress={() => setTimeframe(tf)}
          >
            <Text
              style={[
                styles.timeframeText,
                { color: timeframe === tf ? "#FFFFFF" : colors.textSecondary },
              ]}
            >
              {tf.charAt(0).toUpperCase() + tf.slice(1)}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />}
        showsVerticalScrollIndicator={false}
      >
        {loading && !refreshing ? (
          <View style={{ gap: 14 }}>
            <View style={[styles.summaryCard, { backgroundColor: colors.surface, borderColor: colors.border, padding: 18 }]}>
              <Skeleton width="40%" height={16} style={{ marginBottom: 12 }} />
              <Skeleton width="70%" height={26} style={{ marginBottom: 14 }} />
              <View style={{ flexDirection: "row", gap: 8 }}>
                <Skeleton width="30%" height={24} borderRadius={12} />
                <Skeleton width="30%" height={24} borderRadius={12} />
                <Skeleton width="30%" height={24} borderRadius={12} />
              </View>
            </View>
            <View style={[styles.mealCard, { backgroundColor: colors.surface, borderColor: colors.border, padding: 16 }]}>
              <Skeleton width="50%" height={18} style={{ marginBottom: 10 }} />
              <Skeleton width="80%" height={14} style={{ marginBottom: 8 }} />
              <Skeleton width="35%" height={14} />
            </View>
            <View style={[styles.mealCard, { backgroundColor: colors.surface, borderColor: colors.border, padding: 16 }]}>
              <Skeleton width="45%" height={18} style={{ marginBottom: 10 }} />
              <Skeleton width="75%" height={14} style={{ marginBottom: 8 }} />
              <Skeleton width="30%" height={14} />
            </View>
          </View>
        ) : activeTab === "log" ? (
          <>
            <View style={[styles.summaryCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
              <View style={styles.summaryTop}>
                <Text style={[styles.summaryDate, { color: colors.textSecondary }]}>
                  {timeframe.toUpperCase()} TOTALS
                </Text>
                <Text style={[styles.summaryCalories, { color: colors.primary }]}>
                  {Math.round(totalCalories)} <Text style={styles.unitText}>kcal</Text>
                </Text>
              </View>

              <View style={styles.summaryMacros}>
                <View style={[styles.macroBadgeBox, { backgroundColor: `${colors.indigo}18` }]}>
                  <Text style={[styles.macroLabel, { color: colors.indigo }]}>
                    Protein: {Math.round(totalProtein)}g
                  </Text>
                </View>
                <View style={[styles.macroBadgeBox, { backgroundColor: `${colors.amber}18` }]}>
                  <Text style={[styles.macroLabel, { color: colors.amber }]}>
                    Carbs: {Math.round(totalCarbs)}g
                  </Text>
                </View>
                <View style={[styles.macroBadgeBox, { backgroundColor: `${colors.rose}18` }]}>
                  <Text style={[styles.macroLabel, { color: colors.rose }]}>
                    Fat: {Math.round(totalFat)}g
                  </Text>
                </View>
              </View>
            </View>

            {mealTypes.map((type) => {
              const matchingMeals = meals.filter((m) => m.meal_type.toLowerCase() === type.toLowerCase());

              return (
                <View key={type} style={styles.groupSection}>
                  <View style={styles.groupHeader}>
                    <Text style={[styles.groupTitle, { color: colors.text }]}>{type}</Text>
                    <Text style={[styles.groupCals, { color: colors.textSecondary }]}>
                      {Math.round(matchingMeals.reduce((acc, m) => acc + m.total_calories, 0))} kcal
                    </Text>
                  </View>

                  {matchingMeals.length > 0 ? (
                    matchingMeals.map((meal) => (
                      <View
                        key={meal.id}
                        style={[styles.mealCard, { backgroundColor: colors.surface, borderColor: colors.border }]}
                      >
                        <View style={styles.mealCardHeader}>
                          <View style={styles.mealTitleRow}>
                            <Ionicons name="time-outline" size={14} color={colors.textMuted} />
                            <Text style={[styles.mealTime, { color: colors.textMuted }]}>
                              {formatTime(meal.created_at)} • {formatDateLabel(meal.meal_date)}
                            </Text>
                          </View>

                          <View style={styles.mealActions}>
                            <TouchableOpacity
                              onPress={() => handleDuplicateMeal(meal)}
                              style={styles.iconAction}
                            >
                              <Ionicons name="copy-outline" size={17} color={colors.textSecondary} />
                            </TouchableOpacity>

                            <TouchableOpacity
                              onPress={() => router.push(`/meal/${meal.id}`)}
                              style={styles.iconAction}
                            >
                              <Ionicons name="create-outline" size={17} color={colors.primary} />
                            </TouchableOpacity>

                            <TouchableOpacity
                              onPress={() => handleDeleteMeal(meal.id)}
                              style={styles.iconAction}
                            >
                              <Ionicons name="trash-outline" size={17} color={colors.danger} />
                            </TouchableOpacity>
                          </View>
                        </View>

                        <View style={styles.foodItemList}>
                          {meal.food_items.map((item, idx) => (
                            <View key={idx} style={styles.foodRow}>
                              <Text style={[styles.foodRowName, { color: colors.text }]}>
                                {item.name}
                              </Text>
                              <Text style={[styles.foodRowMeta, { color: colors.textSecondary }]}>
                                {Math.round(item.estimated_weight_g)}g • {Math.round(item.calories)} kcal
                              </Text>
                            </View>
                          ))}
                        </View>

                        <View style={[styles.mealMacroBar, { borderTopColor: colors.surfaceHighlight }]}>
                          <Text style={[styles.macroPillSmall, { color: colors.primary }]}>
                            {Math.round(meal.total_calories)} kcal
                          </Text>
                          <Text style={[styles.macroPillSmall, { color: colors.indigo }]}>
                            P: {Math.round(meal.total_protein)}g
                          </Text>
                          <Text style={[styles.macroPillSmall, { color: colors.amber }]}>
                            C: {Math.round(meal.total_carbs)}g
                          </Text>
                          <Text style={[styles.macroPillSmall, { color: colors.rose }]}>
                            F: {Math.round(meal.total_fat)}g
                          </Text>
                        </View>
                      </View>
                    ))
                  ) : (
                    <View style={[styles.emptyBox, { borderColor: colors.border }]}>
                      <Text style={[styles.emptyText, { color: colors.textMuted }]}>
                        No {type.toLowerCase()} logged
                      </Text>
                    </View>
                  )}
                </View>
              );
            })}
          </>
        ) : (
          <View style={styles.chartsContainer}>
            <View style={[styles.chartCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
              <Text style={[styles.chartTitle, { color: colors.text }]}>Daily Calorie Intake</Text>
              <Text style={[styles.chartSubtitle, { color: colors.textSecondary }]}>
                Average: {summary?.average_daily_calories || 0} kcal / day
              </Text>

              <View style={styles.barGraph}>
                {summary?.daily_stats.map((day, idx) => {
                  const target = day.target_calories || 2000;
                  const ratio = Math.min(1.5, day.calories / target);
                  const barHeight = Math.max(8, Math.min(120, ratio * 90));
                  const isOver = day.calories > target;
                  const dayName = new Date(day.date).toLocaleDateString("en-US", { weekday: "narrow" });

                  return (
                    <View key={idx} style={styles.barCol}>
                      <Text style={[styles.barCalText, { color: colors.textMuted }]}>
                        {day.calories > 0 ? Math.round(day.calories) : ""}
                      </Text>
                      <View style={[styles.barTrack, { backgroundColor: colors.surfaceHighlight }]}>
                        <View
                          style={[
                            styles.barFill,
                            {
                              height: barHeight,
                              backgroundColor: isOver ? colors.amber : colors.primary,
                            },
                          ]}
                        />
                      </View>
                      <Text style={[styles.barDayText, { color: colors.textSecondary }]}>{dayName}</Text>
                    </View>
                  );
                })}
              </View>
            </View>

            <View style={[styles.chartCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
              <Text style={[styles.chartTitle, { color: colors.text }]}>Macro Breakdown</Text>
              <Text style={[styles.chartSubtitle, { color: colors.textSecondary }]}>
                {timeframe.toUpperCase()} Aggregate
              </Text>

              <View style={styles.macroStatRows}>
                <View style={styles.macroStatItem}>
                  <View style={[styles.macroDot, { backgroundColor: colors.indigo }]} />
                  <Text style={[styles.macroStatName, { color: colors.text }]}>Protein</Text>
                  <Text style={[styles.macroStatValue, { color: colors.indigo }]}>
                    {Math.round(summary?.daily_stats.reduce((a, b) => a + b.protein_g, 0) || 0)}g
                  </Text>
                </View>

                <View style={styles.macroStatItem}>
                  <View style={[styles.macroDot, { backgroundColor: colors.amber }]} />
                  <Text style={[styles.macroStatName, { color: colors.text }]}>Carbohydrates</Text>
                  <Text style={[styles.macroStatValue, { color: colors.amber }]}>
                    {Math.round(summary?.daily_stats.reduce((a, b) => a + b.carbs_g, 0) || 0)}g
                  </Text>
                </View>

                <View style={styles.macroStatItem}>
                  <View style={[styles.macroDot, { backgroundColor: colors.rose }]} />
                  <Text style={[styles.macroStatName, { color: colors.text }]}>Fat</Text>
                  <Text style={[styles.macroStatValue, { color: colors.rose }]}>
                    {Math.round(summary?.daily_stats.reduce((a, b) => a + b.fat_g, 0) || 0)}g
                  </Text>
                </View>
              </View>
            </View>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  topBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: "800",
  },
  tabSwitch: {
    flexDirection: "row",
    borderRadius: 12,
    padding: 3,
  },
  switchBtn: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 9,
  },
  switchBtnText: {
    fontSize: 12,
    fontWeight: "700",
  },
  timeframeRow: {
    flexDirection: "row",
    gap: 8,
    paddingHorizontal: 20,
    marginBottom: 12,
  },
  timeframeChip: {
    flex: 1,
    paddingVertical: 8,
    borderRadius: 10,
    borderWidth: 1,
    alignItems: "center",
  },
  timeframeText: {
    fontSize: 12,
    fontWeight: "700",
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 36,
  },
  centerLoading: {
    paddingTop: 80,
    alignItems: "center",
  },
  summaryCard: {
    borderRadius: 18,
    borderWidth: 1,
    padding: 16,
    marginBottom: 16,
  },
  summaryTop: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "baseline",
    marginBottom: 10,
  },
  summaryDate: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
  },
  summaryCalories: {
    fontSize: 24,
    fontWeight: "900",
  },
  unitText: {
    fontSize: 14,
    fontWeight: "600",
  },
  summaryMacros: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  macroBadgeBox: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  macroLabel: {
    fontSize: 12,
    fontWeight: "700",
  },
  groupSection: {
    marginBottom: 18,
  },
  groupHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  groupTitle: {
    fontSize: 16,
    fontWeight: "700",
  },
  groupCals: {
    fontSize: 13,
    fontWeight: "600",
  },
  mealCard: {
    borderRadius: 16,
    borderWidth: 1,
    padding: 14,
    marginBottom: 10,
  },
  mealCardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 10,
  },
  mealTitleRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
  },
  mealTime: {
    fontSize: 11,
    fontWeight: "600",
  },
  mealActions: {
    flexDirection: "row",
    gap: 8,
  },
  iconAction: {
    padding: 4,
  },
  foodItemList: {
    gap: 6,
    marginBottom: 10,
  },
  foodRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  foodRowName: {
    fontSize: 14,
    fontWeight: "600",
  },
  foodRowMeta: {
    fontSize: 12,
  },
  mealMacroBar: {
    flexDirection: "row",
    gap: 12,
    borderTopWidth: 1,
    paddingTop: 8,
  },
  macroPillSmall: {
    fontSize: 11,
    fontWeight: "700",
  },
  emptyBox: {
    borderWidth: 1,
    borderStyle: "dashed",
    borderRadius: 12,
    padding: 14,
    alignItems: "center",
  },
  emptyText: {
    fontSize: 12,
    fontStyle: "italic",
  },
  chartsContainer: {
    gap: 16,
  },
  chartCard: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 18,
  },
  chartTitle: {
    fontSize: 16,
    fontWeight: "800",
    marginBottom: 2,
  },
  chartSubtitle: {
    fontSize: 12,
    marginBottom: 16,
  },
  barGraph: {
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "flex-end",
    height: 160,
    paddingTop: 20,
  },
  barCol: {
    alignItems: "center",
    flex: 1,
  },
  barCalText: {
    fontSize: 9,
    fontWeight: "700",
    marginBottom: 4,
  },
  barTrack: {
    width: 14,
    height: 120,
    borderRadius: 7,
    justifyContent: "flex-end",
    overflow: "hidden",
  },
  barFill: {
    width: "100%",
    borderRadius: 7,
  },
  barDayText: {
    fontSize: 11,
    fontWeight: "600",
    marginTop: 6,
  },
  macroStatRows: {
    gap: 12,
  },
  macroStatItem: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  macroDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    marginRight: 8,
  },
  macroStatName: {
    fontSize: 14,
    fontWeight: "600",
    flex: 1,
  },
  macroStatValue: {
    fontSize: 16,
    fontWeight: "800",
  },
});
