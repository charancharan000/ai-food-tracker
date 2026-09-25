import React, { useState, useEffect, useRef } from "react";
import { View, Text, StyleSheet, Modal, ActivityIndicator, Animated } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../hooks/useTheme";

interface AnalysisLoadingModalProps {
  visible: boolean;
}

const STEPS = [
  { text: "Scanning photo...", icon: "scan-outline" as const },
  { text: "Identifying items...", icon: "restaurant-outline" as const },
  { text: "Estimating portions...", icon: "scale-outline" as const },
  { text: "Calculating nutrition...", icon: "calculator-outline" as const },
];

export const AnalysisLoadingModal: React.FC<AnalysisLoadingModalProps> = ({ visible }) => {
  const { colors } = useTheme();
  const [stepIndex, setStepIndex] = useState(0);

  const pulseScale = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (!visible) {
      setStepIndex(0);
      return;
    }

    const pulseAnim = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseScale, {
          toValue: 1.12,
          duration: 700,
          useNativeDriver: true,
        }),
        Animated.timing(pulseScale, {
          toValue: 1,
          duration: 700,
          useNativeDriver: true,
        }),
      ])
    );
    pulseAnim.start();

    const interval = setInterval(() => {
      setStepIndex((prev) => (prev + 1) % STEPS.length);
    }, 1300);

    return () => {
      clearInterval(interval);
      pulseAnim.stop();
    };
  }, [visible]);

  if (!visible) return null;

  const currentStep = STEPS[stepIndex];

  return (
    <Modal visible={visible} transparent animationType="fade">
      <View style={styles.overlay}>
        <View style={[styles.dialog, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Animated.View
            style={[
              styles.iconCircle,
              {
                backgroundColor: `${colors.primary}18`,
                borderColor: `${colors.primary}35`,
                borderWidth: 1.5,
                transform: [{ scale: pulseScale }],
              },
            ]}
          >
            <Ionicons name={currentStep.icon} size={36} color={colors.primary} />
          </Animated.View>

          <Text style={[styles.title, { color: colors.text }]}>
            {currentStep.text}
          </Text>

          <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
            Identifying ingredients and calculating nutrition breakdown
          </Text>

          <View style={styles.dotsRow}>
            {STEPS.map((_, i) => (
              <View
                key={i}
                style={[
                  styles.dot,
                  {
                    backgroundColor: i === stepIndex ? colors.primary : colors.surfaceHighlight,
                    width: i === stepIndex ? 22 : 8,
                  },
                ]}
              />
            ))}
          </View>

          <ActivityIndicator size="small" color={colors.primary} style={{ marginTop: 14 }} />
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.78)",
    justifyContent: "center",
    alignItems: "center",
    padding: 24,
  },
  dialog: {
    width: "100%",
    maxWidth: 340,
    borderRadius: 24,
    borderWidth: 1,
    padding: 28,
    alignItems: "center",
  },
  iconCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 20,
  },
  title: {
    fontSize: 18,
    fontWeight: "800",
    textAlign: "center",
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 13,
    textAlign: "center",
    lineHeight: 18,
    marginBottom: 20,
  },
  dotsRow: {
    flexDirection: "row",
    gap: 6,
    alignItems: "center",
  },
  dot: {
    height: 8,
    borderRadius: 4,
  },
});
