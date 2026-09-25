import React, { useState, useEffect, useCallback } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../hooks/useTheme";
import { waterService } from "../services/waterService";
import { WaterTodayResponse } from "../types/water";
import { formatTime } from "../utils/formatters";

export default function WaterScreen() {
  const { colors } = useTheme();
  const [data, setData] = useState<WaterTodayResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [loggingAmount, setLoggingAmount] = useState<number | null>(null);

  const loadWater = useCallback(async () => {
    try {
      const res = await waterService.getWaterToday();
      setData(res);
    } catch (e) {
      console.error("Error loading water", e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadWater();
  }, [loadWater]);

  const handleAdd = async (amount: number) => {
    try {
      setLoggingAmount(amount);
      await waterService.logWater(amount);
      await loadWater();
    } catch {
      Alert.alert("Error", "Could not log water.");
    } finally {
      setLoggingAmount(null);
    }
  };

  const handleDelete = async (logId: number) => {
    try {
      await waterService.deleteWaterLog(logId);
      await loadWater();
    } catch {
      Alert.alert("Error", "Could not delete log.");
    }
  };

  const totalLiters = ((data?.total_ml || 0) / 1000).toFixed(1);
  const targetLiters = ((data?.target_ml || 2500) / 1000).toFixed(1);
  const percentage = data?.percentage || 0;

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["bottom"]}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        {/* Main Hydration Progress Card */}
        <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <View style={styles.waterIconCircle}>
            <Ionicons name="water" size={48} color={colors.cyan} />
          </View>

          <Text style={[styles.amountText, { color: colors.text }]}>
            {totalLiters} <Text style={[styles.unit, { color: colors.textSecondary }]}>/ {targetLiters} L</Text>
          </Text>

          <Text style={[styles.percentageText, { color: colors.cyan }]}>
            {percentage}% of Daily Hydration Goal
          </Text>

          {/* Progress Bar */}
          <View style={[styles.track, { backgroundColor: colors.surfaceHighlight }]}>
            <View
              style={[
                styles.fill,
                { width: `${Math.min(100, Math.max(0, percentage))}%`, backgroundColor: colors.cyan },
              ]}
            />
          </View>

          <Text style={[styles.remainingText, { color: colors.textMuted }]}>
            {data?.remaining_ml ? `${(data.remaining_ml / 1000).toFixed(1)} L remaining` : "Daily goal achieved!"}
          </Text>
        </View>

        {/* Quick Add Presets */}
        <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>QUICK ADD WATER</Text>
        <View style={styles.buttonRow}>
          {[250, 500, 750, 1000].map((amt) => (
            <TouchableOpacity
              key={amt}
              style={[styles.quickBtn, { backgroundColor: colors.surface, borderColor: colors.border }]}
              onPress={() => handleAdd(amt)}
              disabled={loggingAmount !== null}
              activeOpacity={0.7}
            >
              {loggingAmount === amt ? (
                <ActivityIndicator size="small" color={colors.cyan} />
              ) : (
                <>
                  <Ionicons name="water-outline" size={18} color={colors.cyan} />
                  <Text style={[styles.quickBtnText, { color: colors.text }]}>+{amt} ml</Text>
                </>
              )}
            </TouchableOpacity>
          ))}
        </View>

        {/* Today's Water Logs */}
        <Text style={[styles.sectionTitle, { color: colors.textSecondary, marginTop: 14 }]}>
          TODAY'S INTAKE HISTORY
        </Text>

        {loading ? (
          <ActivityIndicator size="small" color={colors.cyan} style={{ marginVertical: 20 }} />
        ) : data?.logs && data.logs.length > 0 ? (
          data.logs.map((log) => (
            <View
              key={log.id}
              style={[styles.logRow, { backgroundColor: colors.surface, borderColor: colors.border }]}
            >
              <View style={styles.logLeft}>
                <Ionicons name="checkmark-circle" size={20} color={colors.cyan} />
                <View>
                  <Text style={[styles.logAmount, { color: colors.text }]}>+{log.amount_ml} ml</Text>
                  <Text style={[styles.logTime, { color: colors.textMuted }]}>
                    {formatTime(log.created_at)}
                  </Text>
                </View>
              </View>

              <TouchableOpacity onPress={() => handleDelete(log.id)} style={styles.deleteBtn}>
                <Ionicons name="trash-outline" size={18} color={colors.danger} />
              </TouchableOpacity>
            </View>
          ))
        ) : (
          <View style={[styles.emptyBox, { borderColor: colors.border }]}>
            <Text style={[styles.emptyText, { color: colors.textMuted }]}>
              No water logged today. Tap a quick add button above!
            </Text>
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
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  card: {
    borderRadius: 24,
    borderWidth: 1,
    padding: 24,
    alignItems: "center",
    marginBottom: 20,
  },
  waterIconCircle: {
    width: 84,
    height: 84,
    borderRadius: 42,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(6, 182, 212, 0.15)",
    marginBottom: 16,
  },
  amountText: {
    fontSize: 34,
    fontWeight: "900",
  },
  unit: {
    fontSize: 20,
    fontWeight: "600",
  },
  percentageText: {
    fontSize: 14,
    fontWeight: "700",
    marginTop: 4,
    marginBottom: 16,
  },
  track: {
    width: "100%",
    height: 10,
    borderRadius: 5,
    overflow: "hidden",
    marginBottom: 10,
  },
  fill: {
    height: "100%",
    borderRadius: 5,
  },
  remainingText: {
    fontSize: 12,
    fontWeight: "500",
  },
  sectionTitle: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
    marginBottom: 10,
  },
  buttonRow: {
    flexDirection: "row",
    gap: 8,
    marginBottom: 16,
  },
  quickBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 14,
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: 4,
  },
  quickBtnText: {
    fontSize: 13,
    fontWeight: "700",
  },
  logRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 14,
    borderRadius: 14,
    borderWidth: 1,
    marginBottom: 8,
  },
  logLeft: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },
  logAmount: {
    fontSize: 15,
    fontWeight: "700",
  },
  logTime: {
    fontSize: 11,
    marginTop: 1,
  },
  deleteBtn: {
    padding: 6,
  },
  emptyBox: {
    borderWidth: 1,
    borderStyle: "dashed",
    borderRadius: 14,
    padding: 20,
    alignItems: "center",
  },
  emptyText: {
    fontSize: 13,
    textAlign: "center",
  },
});
