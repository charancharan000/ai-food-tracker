import React, { useEffect, useRef, useState } from "react";
import { View, Text, StyleSheet, Animated, Easing } from "react-native";
import Svg, { Circle, Defs, LinearGradient, Stop } from "react-native-svg";
import { useTheme } from "../hooks/useTheme";

interface MacroRingProps {
  consumed: number;
  target: number;
  size?: number;
  strokeWidth?: number;
}

export const MacroRing: React.FC<MacroRingProps> = ({
  consumed,
  target,
  size = 184,
  strokeWidth = 14,
}) => {
  const { colors } = useTheme();

  const radius = (size - strokeWidth - 8) / 2;
  const circumference = 2 * Math.PI * radius;
  const targetPercentage = target > 0 ? Math.min(1, Math.max(0, consumed / target)) : 0;
  const [animatedPct, setAnimatedPct] = useState(0);
  const animValue = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const anim = Animated.timing(animValue, {
      toValue: targetPercentage,
      duration: 900,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: false,
    });

    const listenerId = animValue.addListener(({ value }) => {
      setAnimatedPct(value);
    });

    anim.start();

    return () => {
      animValue.removeListener(listenerId);
      anim.stop();
    };
  }, [targetPercentage]);

  const strokeDashoffset = circumference - circumference * animatedPct;
  const remaining = Math.max(0, Math.round(target - consumed));

  return (
    <View style={[styles.container, { width: size, height: size }]}>
      <Svg width={size} height={size}>
        <Defs>
          <LinearGradient id="ringGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <Stop offset="0%" stopColor={colors.primaryLight} />
            <Stop offset="100%" stopColor={colors.primary} />
          </LinearGradient>
        </Defs>

        <Circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={colors.primary}
          strokeWidth={strokeWidth + 8}
          strokeOpacity={0.12}
          fill="transparent"
        />

        <Circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={colors.surfaceHighlight}
          strokeWidth={strokeWidth}
          strokeOpacity={0.7}
          fill="transparent"
        />

        <Circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="url(#ringGradient)"
          strokeWidth={strokeWidth}
          strokeDasharray={`${circumference} ${circumference}`}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          fill="transparent"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
      </Svg>

      <View style={styles.centerContent}>
        <Text style={[styles.calorieValue, { color: colors.text }]}>
          {Math.round(consumed).toLocaleString()}
        </Text>
        <Text style={[styles.calorieLabel, { color: colors.textSecondary }]}>
          / {Math.round(target).toLocaleString()} kcal
        </Text>
        <View
          style={[
            styles.remainingBadge,
            {
              backgroundColor: `${colors.primary}18`,
              borderColor: `${colors.primary}35`,
            },
          ]}
        >
          <Text style={[styles.remainingText, { color: colors.primaryLight }]}>
            {remaining.toLocaleString()} left
          </Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
    alignItems: "center",
    position: "relative",
  },
  centerContent: {
    position: "absolute",
    alignItems: "center",
    justifyContent: "center",
  },
  calorieValue: {
    fontSize: 30,
    fontWeight: "900",
    letterSpacing: -0.8,
  },
  calorieLabel: {
    fontSize: 12,
    fontWeight: "600",
    marginTop: 2,
    opacity: 0.85,
  },
  remainingBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 14,
    marginTop: 6,
    borderWidth: 1,
  },
  remainingText: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.3,
  },
});
