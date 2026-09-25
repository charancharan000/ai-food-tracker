import React, { useState, useEffect, useRef } from "react";
import { View, Text, StyleSheet, TouchableOpacity, ActivityIndicator, Animated, Easing } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../hooks/useTheme";
import { waterService } from "../services/waterService";

interface WaterTrackerCardProps {
  consumedMl: number;
  targetMl: number;
  onLogged?: () => void;
}

export const WaterTrackerCard: React.FC<WaterTrackerCardProps> = ({
  consumedMl,
  targetMl,
  onLogged,
}) => {
  const { colors } = useTheme();
  const [loggingAmount, setLoggingAmount] = useState<number | null>(null);

  const targetLiters = (targetMl / 1000).toFixed(1);
  const consumedLiters = (consumedMl / 1000).toFixed(1);
  const percentage = targetMl > 0 ? Math.min(100, Math.round((consumedMl / targetMl) * 100)) : 0;

  const animFill = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(animFill, {
      toValue: percentage,
      duration: 800,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: false,
    }).start();
  }, [percentage]);

  const fillWidth = animFill.interpolate({
    inputRange: [0, 100],
    outputRange: ["0%", "100%"],
    extrapolate: "clamp",
  });

  const handleAddWater = async (amount: number) => {
    try {
      setLoggingAmount(amount);
      await waterService.logWater(amount);
      if (onLogged) onLogged();
    } catch (e) {
      console.error("Failed to log water", e);
    } finally {
      setLoggingAmount(null);
    }
  };

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
      <View style={styles.header}>
        <View style={styles.titleRow}>
          <View style={[styles.iconBox, { backgroundColor: `${colors.cyan}18` }]}>
            <Ionicons name="water" size={20} color={colors.cyan} />
          </View>
          <View>
            <View style={{ flexDirection: "row", alignItems: "center", gap: 6 }}>
              <Text style={[styles.title, { color: colors.text }]}>Hydration</Text>
              <View style={[styles.pctBadge, { backgroundColor: `${colors.cyan}18` }]}>
                <Text style={[styles.pctText, { color: colors.cyan }]}>{percentage}%</Text>
              </View>
            </View>
            <Text style={[styles.amount, { color: colors.textSecondary }]}>
              {consumedLiters} L / {targetLiters} L target
            </Text>
          </View>
        </View>

        <View style={styles.buttonGroup}>
          <TouchableOpacity
            style={[styles.quickBtn, { backgroundColor: colors.surfaceHighlight }]}
            onPress={() => handleAddWater(250)}
            disabled={loggingAmount !== null}
            activeOpacity={0.7}
          >
            {loggingAmount === 250 ? (
              <ActivityIndicator size="small" color={colors.cyan} />
            ) : (
              <Text style={[styles.quickBtnText, { color: colors.cyan }]}>+250ml</Text>
            )}
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.quickBtn,
              {
                backgroundColor: `${colors.cyan}20`,
                borderColor: `${colors.cyan}35`,
                borderWidth: 1,
              },
            ]}
            onPress={() => handleAddWater(500)}
            disabled={loggingAmount !== null}
            activeOpacity={0.7}
          >
            {loggingAmount === 500 ? (
              <ActivityIndicator size="small" color={colors.cyan} />
            ) : (
              <Text style={[styles.quickBtnText, { color: colors.cyan }]}>+500ml</Text>
            )}
          </TouchableOpacity>
        </View>
      </View>

      {/* Animated Water Bar */}
      <View style={[styles.track, { backgroundColor: colors.surfaceHighlight }]}>
        <Animated.View
          style={[
            styles.fill,
            {
              width: fillWidth,
              backgroundColor: colors.cyan,
            },
          ]}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 16,
    marginBottom: 16,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },
  titleRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  iconBox: {
    width: 42,
    height: 42,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 12,
  },
  title: {
    fontSize: 16,
    fontWeight: "800",
    letterSpacing: -0.2,
  },
  pctBadge: {
    paddingHorizontal: 6,
    paddingVertical: 1,
    borderRadius: 6,
  },
  pctText: {
    fontSize: 10,
    fontWeight: "800",
  },
  amount: {
    fontSize: 12,
    fontWeight: "500",
    marginTop: 2,
  },
  buttonGroup: {
    flexDirection: "row",
    gap: 8,
  },
  quickBtn: {
    paddingHorizontal: 12,
    paddingVertical: 7,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
    minWidth: 66,
  },
  quickBtnText: {
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 0.2,
  },
  track: {
    height: 8,
    borderRadius: 4,
    overflow: "hidden",
  },
  fill: {
    height: "100%",
    borderRadius: 4,
  },
});
