import React, { useEffect, useRef } from "react";
import { View, Text, StyleSheet, Animated, Easing } from "react-native";
import { useTheme } from "../hooks/useTheme";

interface MacroCardProps {
  label: string;
  consumed: number;
  target: number;
  color: string;
  unit?: string;
}

export const MacroCard: React.FC<MacroCardProps> = ({
  label,
  consumed,
  target,
  color,
  unit = "g",
}) => {
  const { colors } = useTheme();

  const percentage = target > 0 ? Math.min(100, Math.round((consumed / target) * 100)) : 0;
  const remaining = Math.max(0, Math.round(target - consumed));

  const animWidth = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(animWidth, {
      toValue: percentage,
      duration: 850,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: false,
    }).start();
  }, [percentage]);

  const widthInterpolation = animWidth.interpolate({
    inputRange: [0, 100],
    outputRange: ["0%", "100%"],
    extrapolate: "clamp",
  });

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
          <View style={[styles.indicator, { backgroundColor: color, shadowColor: color }]} />
          <Text style={[styles.label, { color: colors.textSecondary }]}>{label}</Text>
        </View>
        <View style={[styles.pctBadge, { backgroundColor: `${color}18` }]}>
          <Text style={[styles.percentage, { color }]}>{percentage}%</Text>
        </View>
      </View>

      <View style={styles.amountRow}>
        <Text style={[styles.consumed, { color: colors.text }]}>
          {Math.round(consumed)}
        </Text>
        <Text style={[styles.target, { color: colors.textMuted }]}>
          {" "}/ {Math.round(target)}{unit}
        </Text>
      </View>

      <View style={[styles.progressTrack, { backgroundColor: colors.surfaceHighlight }]}>
        <Animated.View
          style={[
            styles.progressBar,
            {
              width: widthInterpolation,
              backgroundColor: color,
            },
          ]}
        />
      </View>

      <Text style={[styles.remaining, { color: colors.textMuted }]}>
        {remaining}{unit} remaining
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    flex: 1,
    padding: 14,
    borderRadius: 20,
    borderWidth: 1,
    minWidth: 100,
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  titleRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  indicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.8,
    shadowRadius: 4,
  },
  label: {
    fontSize: 11,
    fontWeight: "700",
    textTransform: "uppercase",
    letterSpacing: 0.6,
  },
  pctBadge: {
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 8,
  },
  percentage: {
    fontSize: 11,
    fontWeight: "800",
  },
  amountRow: {
    flexDirection: "row",
    alignItems: "baseline",
    marginBottom: 8,
  },
  consumed: {
    fontSize: 18,
    fontWeight: "900",
    letterSpacing: -0.3,
  },
  target: {
    fontSize: 12,
    fontWeight: "600",
  },
  progressTrack: {
    height: 6,
    borderRadius: 3,
    overflow: "hidden",
    marginBottom: 6,
  },
  progressBar: {
    height: "100%",
    borderRadius: 3,
  },
  remaining: {
    fontSize: 10,
    fontWeight: "600",
    letterSpacing: 0.1,
  },
});
