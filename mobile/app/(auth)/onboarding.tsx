import React, { useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity, Dimensions } from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../../hooks/useTheme";

const { width } = Dimensions.get("window");

const SLIDES = [
  {
    icon: "camera" as const,
    title: "Snap & Analyze Meals",
    description: "Take a photo of any dish. Multimodal AI identifies food items, estimates portions, and calculates nutrition instantly.",
    color: "#10B981",
  },
  {
    icon: "options" as const,
    title: "Flexible Portion Control",
    description: "Adjust grams, servings, or choose presets. Calories and macronutrients scale proportionally in real-time.",
    color: "#6366F1",
  },
  {
    icon: "analytics" as const,
    title: "Hit Your Daily Targets",
    description: "Personalized calorie goals, macro targets, and water tracking help you lose, maintain, or build muscle effortlessly.",
    color: "#06B6D4",
  },
];

export default function OnboardingScreen() {
  const { colors } = useTheme();
  const router = useRouter();
  const [currentIndex, setCurrentIndex] = useState(0);

  const handleNext = () => {
    if (currentIndex < SLIDES.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      router.push("/(auth)/register");
    }
  };

  const slide = SLIDES[currentIndex];

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={styles.topBar}>
        <Text style={[styles.brand, { color: colors.text }]}>
          NutriScan <Text style={{ color: colors.primary }}>AI</Text>
        </Text>
        <TouchableOpacity onPress={() => router.push("/(auth)/login")}>
          <Text style={[styles.skipText, { color: colors.primary }]}>Skip</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.centerSection}>
        <View style={[styles.iconWrapper, { backgroundColor: `${slide.color}20` }]}>
          <Ionicons name={slide.icon} size={64} color={slide.color} />
        </View>

        <Text style={[styles.slideTitle, { color: colors.text }]}>{slide.title}</Text>
        <Text style={[styles.slideDescription, { color: colors.textSecondary }]}>
          {slide.description}
        </Text>

        {/* Indicators */}
        <View style={styles.dotsRow}>
          {SLIDES.map((_, i) => (
            <View
              key={i}
              style={[
                styles.dot,
                {
                  backgroundColor: i === currentIndex ? colors.primary : colors.surfaceHighlight,
                  width: i === currentIndex ? 24 : 8,
                },
              ]}
            />
          ))}
        </View>
      </View>

      <View style={styles.bottomSection}>
        <TouchableOpacity
          style={[styles.primaryButton, { backgroundColor: colors.primary }]}
          onPress={handleNext}
          activeOpacity={0.8}
        >
          <Text style={styles.primaryButtonText}>
            {currentIndex === SLIDES.length - 1 ? "Get Started" : "Continue"}
          </Text>
          <Ionicons name="arrow-forward" size={18} color="#FFFFFF" />
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.secondaryButton}
          onPress={() => router.push("/(auth)/login")}
          activeOpacity={0.7}
        >
          <Text style={[styles.secondaryButtonText, { color: colors.textSecondary }]}>
            Already have an account? <Text style={{ color: colors.primary, fontWeight: "700" }}>Log In</Text>
          </Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 24,
    justifyContent: "space-between",
  },
  topBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 12,
  },
  brand: {
    fontSize: 20,
    fontWeight: "800",
  },
  skipText: {
    fontSize: 14,
    fontWeight: "700",
  },
  centerSection: {
    alignItems: "center",
    paddingHorizontal: 12,
  },
  iconWrapper: {
    width: 130,
    height: 130,
    borderRadius: 65,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 32,
  },
  slideTitle: {
    fontSize: 26,
    fontWeight: "800",
    textAlign: "center",
    marginBottom: 12,
    letterSpacing: -0.5,
  },
  slideDescription: {
    fontSize: 15,
    lineHeight: 22,
    textAlign: "center",
    marginBottom: 32,
  },
  dotsRow: {
    flexDirection: "row",
    gap: 8,
    alignItems: "center",
  },
  dot: {
    height: 8,
    borderRadius: 4,
  },
  bottomSection: {
    paddingBottom: 24,
    gap: 16,
  },
  primaryButton: {
    height: 54,
    borderRadius: 16,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
  },
  primaryButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
  secondaryButton: {
    alignItems: "center",
    paddingVertical: 8,
  },
  secondaryButtonText: {
    fontSize: 14,
  },
});
