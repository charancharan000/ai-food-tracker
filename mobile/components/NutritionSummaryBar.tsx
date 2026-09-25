import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { useTheme } from "../hooks/useTheme";
import { NutritionTotal } from "../types/food";

interface NutritionSummaryBarProps {
  total: NutritionTotal;
}

export const NutritionSummaryBar: React.FC<NutritionSummaryBarProps> = ({ total }) => {
  const { colors } = useTheme();

  return (
    <View style={[styles.container, { backgroundColor: colors.surface, borderColor: colors.border }]}>
      <View style={styles.metricItem}>
        <Text style={[styles.metricLabel, { color: colors.textSecondary }]}>CALORIES</Text>
        <Text style={[styles.metricValue, { color: colors.primary }]}>
          {Math.round(total.calories)} <Text style={styles.unit}>kcal</Text>
        </Text>
      </View>

      <View style={[styles.divider, { backgroundColor: colors.border }]} />

      <View style={styles.metricItem}>
        <Text style={[styles.metricLabel, { color: colors.textSecondary }]}>PROTEIN</Text>
        <Text style={[styles.metricValue, { color: colors.indigo }]}>
          {Math.round(total.protein_g)} <Text style={styles.unit}>g</Text>
        </Text>
      </View>

      <View style={[styles.divider, { backgroundColor: colors.border }]} />

      <View style={styles.metricItem}>
        <Text style={[styles.metricLabel, { color: colors.textSecondary }]}>CARBS</Text>
        <Text style={[styles.metricValue, { color: colors.amber }]}>
          {Math.round(total.carbs_g)} <Text style={styles.unit}>g</Text>
        </Text>
      </View>

      <View style={[styles.divider, { backgroundColor: colors.border }]} />

      <View style={styles.metricItem}>
        <Text style={[styles.metricLabel, { color: colors.textSecondary }]}>FAT</Text>
        <Text style={[styles.metricValue, { color: colors.rose }]}>
          {Math.round(total.fat_g)} <Text style={styles.unit}>g</Text>
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    borderRadius: 20,
    borderWidth: 1,
    paddingVertical: 14,
    paddingHorizontal: 8,
    marginVertical: 12,
    alignItems: "center",
    justifyContent: "space-around",
  },
  metricItem: {
    alignItems: "center",
    flex: 1,
  },
  metricLabel: {
    fontSize: 10,
    fontWeight: "700",
    letterSpacing: 0.5,
    marginBottom: 2,
  },
  metricValue: {
    fontSize: 17,
    fontWeight: "800",
  },
  unit: {
    fontSize: 11,
    fontWeight: "500",
  },
  divider: {
    width: 1,
    height: 24,
  },
});
