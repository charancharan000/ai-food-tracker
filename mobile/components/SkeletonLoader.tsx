import React, { useEffect, useRef } from "react";
import { View, Animated, StyleSheet, StyleProp, ViewStyle } from "react-native";
import { useTheme } from "../hooks/useTheme";

interface SkeletonProps {
  width?: number | string;
  height?: number;
  borderRadius?: number;
  style?: StyleProp<ViewStyle>;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  width = "100%",
  height = 20,
  borderRadius = 8,
  style,
}) => {
  const { colors } = useTheme();
  const opacityAnim = useRef(new Animated.Value(0.3)).current;

  useEffect(() => {
    const pulse = Animated.loop(
      Animated.sequence([
        Animated.timing(opacityAnim, {
          toValue: 0.75,
          duration: 750,
          useNativeDriver: true,
        }),
        Animated.timing(opacityAnim, {
          toValue: 0.3,
          duration: 750,
          useNativeDriver: true,
        }),
      ])
    );
    pulse.start();

    return () => pulse.stop();
  }, [opacityAnim]);

  return (
    <Animated.View
      style={[
        {
          width: width as any,
          height,
          borderRadius,
          backgroundColor: colors.surfaceHighlight,
          opacity: opacityAnim,
        },
        style,
      ]}
    />
  );
};

export const DashboardSkeleton: React.FC = () => {
  const { colors } = useTheme();

  return (
    <View style={styles.container}>
      {/* Top Banner Skeleton */}
      <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
        <View style={styles.row}>
          <Skeleton width={160} height={160} borderRadius={80} />
          <View style={styles.column}>
            <Skeleton width="90%" height={24} style={{ marginBottom: 12 }} />
            <Skeleton width="70%" height={16} style={{ marginBottom: 10 }} />
            <Skeleton width="50%" height={28} borderRadius={14} />
          </View>
        </View>
      </View>

      {/* Macro Row Skeletons */}
      <View style={styles.macroRow}>
        <View style={[styles.miniCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Skeleton width="60%" height={14} style={{ marginBottom: 8 }} />
          <Skeleton width="80%" height={22} style={{ marginBottom: 8 }} />
          <Skeleton width="100%" height={6} borderRadius={3} />
        </View>
        <View style={[styles.miniCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Skeleton width="60%" height={14} style={{ marginBottom: 8 }} />
          <Skeleton width="80%" height={22} style={{ marginBottom: 8 }} />
          <Skeleton width="100%" height={6} borderRadius={3} />
        </View>
        <View style={[styles.miniCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Skeleton width="60%" height={14} style={{ marginBottom: 8 }} />
          <Skeleton width="80%" height={22} style={{ marginBottom: 8 }} />
          <Skeleton width="100%" height={6} borderRadius={3} />
        </View>
      </View>

      {/* Water Card Skeleton */}
      <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border, height: 110 }]}>
        <Skeleton width="40%" height={18} style={{ marginBottom: 12 }} />
        <Skeleton width="75%" height={24} style={{ marginBottom: 10 }} />
        <Skeleton width="100%" height={8} borderRadius={4} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    gap: 16,
  },
  card: {
    padding: 18,
    borderRadius: 24,
    borderWidth: 1,
  },
  row: {
    flexDirection: "row",
    alignItems: "center",
    gap: 18,
  },
  column: {
    flex: 1,
  },
  macroRow: {
    flexDirection: "row",
    gap: 10,
  },
  miniCard: {
    flex: 1,
    padding: 14,
    borderRadius: 20,
    borderWidth: 1,
  },
});
