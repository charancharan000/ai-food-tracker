import React, { useState, useEffect, useCallback } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  ActivityIndicator,
  Image,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useAuth } from "../../hooks/useAuth";
import { useTheme } from "../../hooks/useTheme";
import { dashboardService } from "../../services/dashboardService";
import { DashboardToday } from "../../types/dashboard";
import { Meal, MealType } from "../../types/food";
import { MacroRing } from "../../components/MacroRing";
import { MacroCard } from "../../components/MacroCard";
import { MealCard } from "../../components/MealCard";
import { WaterTrackerCard } from "../../components/WaterTrackerCard";
import { ThemeToggle } from "../../components/ThemeToggle";
import { DashboardSkeleton } from "../../components/SkeletonLoader";

export default function HomeDashboardScreen() {
  const { user } = useAuth();
  const { colors } = useTheme();
  const router = useRouter();

  const [dashboard, setDashboard] = useState<DashboardToday | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchDashboard = useCallback(async () => {
    try {
      const data = await dashboardService.getDashboardToday();
      setDashboard(data);
    } catch (e) {
      console.warn("Error fetching dashboard data", e);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  const onRefresh = () => {
    setRefreshing(true);
    fetchDashboard();
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
  };

  const firstName = user?.name ? user.name.split(" ")[0] : "Friend";

  const standardMealTypes: MealType[] = ["Breakfast", "Lunch", "Snack", "Dinner"];

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      <View style={styles.topHeader}>
        <View>
          <Image
            source={require("../../assets/logo.png")}
            style={{ width: 115, height: 32, marginBottom: 4 }}
            resizeMode="contain"
          />
          <Text style={[styles.greetingSubtitle, { color: colors.textSecondary }]}>
            {getGreeting()}, {firstName} 👋
          </Text>
        </View>

        <View style={styles.headerActions}>
          <ThemeToggle />
          <TouchableOpacity
            style={[
              styles.quickScanBtn,
              {
                backgroundColor: colors.primary,
                shadowColor: colors.primary,
              },
            ]}
            onPress={() => router.push("/(tabs)/scan")}
            activeOpacity={0.8}
          >
            <Ionicons name="camera-outline" size={17} color="#FFFFFF" />
            <Text style={styles.quickScanBtnText}>+ Scan</Text>
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />}
        showsVerticalScrollIndicator={false}
      >
        {loading && !refreshing ? (
          <DashboardSkeleton />
        ) : (
          <>
            <View
              style={[
                styles.heroCard,
                {
                  backgroundColor: colors.surface,
                  borderColor: colors.border,
                },
              ]}
            >
              <View style={styles.heroHeader}>
                <View style={styles.heroTitleRow}>
                  <Ionicons name="flame" size={16} color={colors.primary} />
                  <Text style={[styles.heroTitle, { color: colors.textSecondary }]}>TODAY'S CALORIES</Text>
                </View>
                <View style={[styles.statusBadge, { backgroundColor: `${colors.primary}18` }]}>
                  <Text style={[styles.statusBadgeText, { color: colors.primaryLight }]}>
                    Target: {dashboard?.daily_calorie_target || 2000} kcal
                  </Text>
                </View>
              </View>

              <View style={styles.ringContainer}>
                <MacroRing
                  consumed={dashboard?.calories_consumed || 0}
                  target={dashboard?.daily_calorie_target || 2000}
                />
              </View>

              <View style={[styles.statsStrip, { borderTopColor: colors.surfaceHighlight }]}>
                <View style={styles.statBox}>
                  <Text style={[styles.statNum, { color: colors.text }]}>
                    {Math.round(dashboard?.calories_consumed || 0)}
                  </Text>
                  <Text style={[styles.statLbl, { color: colors.textSecondary }]}>Consumed</Text>
                </View>
                <View style={[styles.verticalDivider, { backgroundColor: colors.border }]} />
                <View style={styles.statBox}>
                  <Text style={[styles.statNum, { color: colors.primary }]}>
                    {Math.round(dashboard?.calories_remaining || 0)}
                  </Text>
                  <Text style={[styles.statLbl, { color: colors.textSecondary }]}>Remaining</Text>
                </View>
                <View style={[styles.verticalDivider, { backgroundColor: colors.border }]} />
                <View style={styles.statBox}>
                  <Text style={[styles.statNum, { color: colors.indigo }]}>
                    {Math.round(dashboard?.protein?.remaining || 0)}g
                  </Text>
                  <Text style={[styles.statLbl, { color: colors.textSecondary }]}>P Left</Text>
                </View>
              </View>
            </View>

            <View style={styles.sectionHeader}>
              <Text style={[styles.sectionHeading, { color: colors.text }]}>Macronutrients</Text>
            </View>

            <View style={styles.macroCardsRow}>
              <MacroCard
                label="Protein"
                consumed={dashboard?.protein?.consumed || 0}
                target={dashboard?.protein?.target || 150}
                color={colors.indigo}
              />
              <MacroCard
                label="Carbs"
                consumed={dashboard?.carbs?.consumed || 0}
                target={dashboard?.carbs?.target || 250}
                color={colors.amber}
              />
              <MacroCard
                label="Fat"
                consumed={dashboard?.fat?.consumed || 0}
                target={dashboard?.fat?.target || 65}
                color={colors.rose}
              />
            </View>

            <WaterTrackerCard
              consumedMl={dashboard?.water_consumed_ml || 0}
              targetMl={dashboard?.water_target_ml || 2500}
              onLogged={fetchDashboard}
            />

            <View style={styles.sectionHeader}>
              <Text style={[styles.sectionHeading, { color: colors.text }]}>Today's Meals</Text>
              <TouchableOpacity onPress={() => router.push("/(tabs)/history")}>
                <Text style={[styles.viewLogLink, { color: colors.primary }]}>View Food Log</Text>
              </TouchableOpacity>
            </View>

            {standardMealTypes.map((type) => {
              const mealGroup = dashboard?.meals_by_type?.[type] || { calories: 0, count: 0, meals: [] };
              return (
                <MealCard
                  key={type}
                  mealType={type}
                  calories={mealGroup.calories}
                  meals={mealGroup.meals}
                  onAddPress={() => {
                    router.push({
                      pathname: "/(tabs)/scan",
                      params: { preferredMealType: type },
                    });
                  }}
                  onMealPress={(m: Meal) => {
                    router.push(`/meal/${m.id}`);
                  }}
                />
              );
            })}
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  topHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    paddingTop: 8,
    paddingBottom: 12,
  },
  greetingSubtitle: {
    fontSize: 13,
    fontWeight: "600",
  },
  greetingName: {
    fontSize: 22,
    fontWeight: "900",
    letterSpacing: -0.5,
  },
  headerActions: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
  },
  quickScanBtn: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    gap: 5,
    elevation: 4,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 5,
  },
  quickScanBtnText: {
    color: "#FFFFFF",
    fontSize: 13,
    fontWeight: "800",
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 32,
  },
  centerLoading: {
    paddingTop: 80,
    alignItems: "center",
  },
  loadingText: {
    marginTop: 12,
    fontSize: 14,
    fontWeight: "500",
  },
  heroCard: {
    borderRadius: 24,
    borderWidth: 1,
    paddingTop: 18,
    marginBottom: 20,
    overflow: "hidden",
  },
  heroHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    marginBottom: 10,
  },
  heroTitleRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },
  heroTitle: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
  },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusBadgeText: {
    fontSize: 11,
    fontWeight: "700",
  },
  ringContainer: {
    alignItems: "center",
    marginVertical: 10,
  },
  statsStrip: {
    flexDirection: "row",
    borderTopWidth: 1,
    paddingVertical: 14,
    paddingHorizontal: 10,
  },
  statBox: {
    flex: 1,
    alignItems: "center",
  },
  statNum: {
    fontSize: 18,
    fontWeight: "900",
    letterSpacing: -0.3,
  },
  statLbl: {
    fontSize: 11,
    fontWeight: "600",
    marginTop: 2,
  },
  verticalDivider: {
    width: 1,
    height: "75%",
    alignSelf: "center",
  },
  sectionHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
    marginTop: 6,
  },
  sectionHeading: {
    fontSize: 18,
    fontWeight: "900",
    letterSpacing: -0.3,
  },
  viewLogLink: {
    fontSize: 13,
    fontWeight: "700",
  },
  macroCardsRow: {
    flexDirection: "row",
    gap: 10,
    marginBottom: 20,
  },
});
