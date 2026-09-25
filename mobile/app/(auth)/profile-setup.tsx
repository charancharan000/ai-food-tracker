import React, { useState, useMemo } from "react";
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { useRouter, useLocalSearchParams } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useAuth } from "../../hooks/useAuth";
import { useTheme } from "../../hooks/useTheme";
import { estimateCalorieTargets } from "../../utils/nutrition";

export default function ProfileSetupScreen() {
  const { register } = useAuth();
  const { colors } = useTheme();
  const router = useRouter();
  const params = useLocalSearchParams<{ name?: string; email?: string; password?: string }>();

  const [age, setAge] = useState("28");
  const [gender, setGender] = useState<"male" | "female" | "other">("male");
  const [height, setHeight] = useState("175");
  const [weight, setWeight] = useState("70");
  const [activity, setActivity] = useState<"sedentary" | "light" | "moderate" | "active" | "very_active">("moderate");
  const [goal, setGoal] = useState<"lose" | "maintain" | "gain">("maintain");
  const [customCalorieTarget, setCustomCalorieTarget] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Compute estimated targets dynamically
  const estimated = useMemo(() => {
    const a = parseInt(age, 10) || 28;
    const h = parseFloat(height) || 175;
    const w = parseFloat(weight) || 70;
    return estimateCalorieTargets(a, gender, h, w, activity, goal);
  }, [age, gender, height, weight, activity, goal]);

  const activeCalorieTarget = customCalorieTarget ? parseInt(customCalorieTarget, 10) || estimated.calories : estimated.calories;

  const handleFinishRegistration = async () => {
    if (!params.email || !params.password) {
      setErrorMsg("Missing account registration credentials. Please go back.");
      return;
    }

    try {
      setIsLoading(true);
      setErrorMsg(null);

      await register({
        name: params.name || "User",
        email: params.email,
        password: params.password,
        age: parseInt(age, 10) || 28,
        gender,
        height_cm: parseFloat(height) || 175,
        weight_kg: parseFloat(weight) || 70,
        activity_level: activity,
        goal,
      });

      router.replace("/(tabs)");
    } catch (e: any) {
      const msg = e.response?.data?.detail || "Registration failed. Please try again.";
      setErrorMsg(msg);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        <ScrollView contentContainerStyle={styles.scrollContent} keyboardShouldPersistTaps="handled">
          <View style={styles.header}>
            <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
              <Ionicons name="arrow-back" size={24} color={colors.text} />
            </TouchableOpacity>
            <Text style={[styles.title, { color: colors.text }]}>Personalize Your Targets</Text>
            <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
              Tell us about yourself so NutriScan AI can tailor your daily calorie & macro goals
            </Text>
          </View>

          {errorMsg && (
            <View style={[styles.errorBox, { backgroundColor: `${colors.danger}15`, borderColor: colors.danger }]}>
              <Ionicons name="alert-circle" size={18} color={colors.danger} />
              <Text style={[styles.errorText, { color: colors.danger }]}>{errorMsg}</Text>
            </View>
          )}

          {/* Goal Selector */}
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>PRIMARY FITNESS GOAL</Text>
            <View style={styles.optionsRow}>
              {[
                { key: "lose", label: "Lose Weight", icon: "trending-down-outline" },
                { key: "maintain", label: "Maintain Weight", icon: "pause-outline" },
                { key: "gain", label: "Gain Weight", icon: "trending-up-outline" },
              ].map((item) => (
                <TouchableOpacity
                  key={item.key}
                  style={[
                    styles.optionCard,
                    {
                      backgroundColor: goal === item.key ? colors.primary : colors.surface,
                      borderColor: goal === item.key ? colors.primary : colors.border,
                    },
                  ]}
                  onPress={() => setGoal(item.key as any)}
                >
                  <Ionicons
                    name={item.icon as any}
                    size={20}
                    color={goal === item.key ? "#FFFFFF" : colors.text}
                  />
                  <Text
                    style={[
                      styles.optionLabel,
                      { color: goal === item.key ? "#FFFFFF" : colors.text },
                    ]}
                  >
                    {item.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Gender Selector */}
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>GENDER</Text>
            <View style={styles.optionsRow}>
              {["male", "female", "other"].map((g) => (
                <TouchableOpacity
                  key={g}
                  style={[
                    styles.optionCard,
                    {
                      backgroundColor: gender === g ? colors.primary : colors.surface,
                      borderColor: gender === g ? colors.primary : colors.border,
                    },
                  ]}
                  onPress={() => setGender(g as any)}
                >
                  <Text
                    style={[
                      styles.optionLabel,
                      { color: gender === g ? "#FFFFFF" : colors.text, textTransform: "capitalize" },
                    ]}
                  >
                    {g}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Biometrics Input Grid */}
          <View style={styles.grid}>
            <View style={styles.gridCol}>
              <Text style={[styles.label, { color: colors.textSecondary }]}>AGE</Text>
              <View style={[styles.inputBox, { backgroundColor: colors.surface, borderColor: colors.border }]}>
                <TextInput
                  style={[styles.input, { color: colors.text }]}
                  keyboardType="numeric"
                  value={age}
                  onChangeText={setAge}
                />
                <Text style={[styles.unit, { color: colors.textMuted }]}>yrs</Text>
              </View>
            </View>

            <View style={styles.gridCol}>
              <Text style={[styles.label, { color: colors.textSecondary }]}>HEIGHT</Text>
              <View style={[styles.inputBox, { backgroundColor: colors.surface, borderColor: colors.border }]}>
                <TextInput
                  style={[styles.input, { color: colors.text }]}
                  keyboardType="numeric"
                  value={height}
                  onChangeText={setHeight}
                />
                <Text style={[styles.unit, { color: colors.textMuted }]}>cm</Text>
              </View>
            </View>

            <View style={styles.gridCol}>
              <Text style={[styles.label, { color: colors.textSecondary }]}>WEIGHT</Text>
              <View style={[styles.inputBox, { backgroundColor: colors.surface, borderColor: colors.border }]}>
                <TextInput
                  style={[styles.input, { color: colors.text }]}
                  keyboardType="numeric"
                  value={weight}
                  onChangeText={setWeight}
                />
                <Text style={[styles.unit, { color: colors.textMuted }]}>kg</Text>
              </View>
            </View>
          </View>

          {/* Activity Level */}
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>ACTIVITY LEVEL</Text>
            <View style={styles.verticalOptions}>
              {[
                { key: "sedentary", label: "Sedentary (desk job, little exercise)" },
                { key: "light", label: "Lightly Active (1-3 days/week exercise)" },
                { key: "moderate", label: "Moderately Active (3-5 days/week)" },
                { key: "active", label: "Very Active (6-7 days/week hard exercise)" },
              ].map((item) => (
                <TouchableOpacity
                  key={item.key}
                  style={[
                    styles.verticalOptionCard,
                    {
                      backgroundColor: activity === item.key ? `${colors.primary}15` : colors.surface,
                      borderColor: activity === item.key ? colors.primary : colors.border,
                    },
                  ]}
                  onPress={() => setActivity(item.key as any)}
                >
                  <Ionicons
                    name={activity === item.key ? "checkmark-circle" : "ellipse-outline"}
                    size={20}
                    color={activity === item.key ? colors.primary : colors.textMuted}
                  />
                  <Text style={[styles.verticalOptionText, { color: colors.text }]}>{item.label}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* AI Calculated Target Display & Custom Override */}
          <View style={[styles.targetCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
            <View style={styles.targetHeader}>
              <Ionicons name="sparkles" size={20} color={colors.primary} />
              <Text style={[styles.targetTitle, { color: colors.text }]}>Estimated Daily Target</Text>
            </View>

            <Text style={[styles.targetNumber, { color: colors.primary }]}>
              {activeCalorieTarget} <Text style={styles.targetUnit}>kcal / day</Text>
            </Text>

            <View style={styles.macroPills}>
              <Text style={[styles.targetMacro, { color: colors.indigo }]}>
                Protein: {estimated.protein}g
              </Text>
              <Text style={[styles.targetMacro, { color: colors.amber }]}>
                Carbs: {estimated.carbs}g
              </Text>
              <Text style={[styles.targetMacro, { color: colors.rose }]}>
                Fat: {estimated.fat}g
              </Text>
              <Text style={[styles.targetMacro, { color: colors.cyan }]}>
                Water: {(estimated.water / 1000).toFixed(1)}L
              </Text>
            </View>

            <View style={styles.overrideSection}>
              <Text style={[styles.overrideLabel, { color: colors.textSecondary }]}>
                Manual Calorie Override (Optional):
              </Text>
              <TextInput
                style={[styles.overrideInput, { backgroundColor: colors.surfaceHighlight, color: colors.text }]}
                placeholder={`${estimated.calories}`}
                placeholderTextColor={colors.textMuted}
                keyboardType="numeric"
                value={customCalorieTarget}
                onChangeText={setCustomCalorieTarget}
              />
            </View>
          </View>

          {/* Complete Button */}
          <TouchableOpacity
            style={[styles.finishBtn, { backgroundColor: colors.primary }]}
            onPress={handleFinishRegistration}
            disabled={isLoading}
            activeOpacity={0.8}
          >
            {isLoading ? (
              <ActivityIndicator color="#FFFFFF" />
            ) : (
              <Text style={styles.finishBtnText}>Complete Profile & Launch NutriScan</Text>
            )}
          </TouchableOpacity>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingVertical: 16,
    paddingBottom: 40,
  },
  header: {
    marginBottom: 20,
  },
  backBtn: {
    marginBottom: 10,
    width: 36,
    height: 36,
    justifyContent: "center",
  },
  title: {
    fontSize: 24,
    fontWeight: "800",
    marginBottom: 6,
  },
  subtitle: {
    fontSize: 14,
    lineHeight: 20,
  },
  errorBox: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    marginBottom: 16,
    gap: 8,
  },
  errorText: {
    fontSize: 13,
    flex: 1,
  },
  section: {
    marginBottom: 18,
  },
  sectionTitle: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
    marginBottom: 8,
  },
  optionsRow: {
    flexDirection: "row",
    gap: 8,
  },
  optionCard: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 8,
    borderRadius: 12,
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: 4,
  },
  optionLabel: {
    fontSize: 12,
    fontWeight: "700",
    textAlign: "center",
  },
  grid: {
    flexDirection: "row",
    gap: 10,
    marginBottom: 18,
  },
  gridCol: {
    flex: 1,
  },
  label: {
    fontSize: 11,
    fontWeight: "700",
    marginBottom: 6,
  },
  inputBox: {
    flexDirection: "row",
    alignItems: "center",
    borderRadius: 12,
    borderWidth: 1,
    paddingHorizontal: 12,
    height: 48,
  },
  input: {
    flex: 1,
    fontSize: 16,
    fontWeight: "700",
  },
  unit: {
    fontSize: 12,
    fontWeight: "600",
  },
  verticalOptions: {
    gap: 8,
  },
  verticalOptionCard: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    gap: 10,
  },
  verticalOptionText: {
    fontSize: 13,
    fontWeight: "600",
    flex: 1,
  },
  targetCard: {
    borderRadius: 18,
    borderWidth: 1,
    padding: 18,
    marginVertical: 14,
  },
  targetHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 8,
  },
  targetTitle: {
    fontSize: 14,
    fontWeight: "700",
  },
  targetNumber: {
    fontSize: 32,
    fontWeight: "900",
    marginBottom: 8,
  },
  targetUnit: {
    fontSize: 14,
    fontWeight: "600",
  },
  macroPills: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 12,
    marginBottom: 16,
  },
  targetMacro: {
    fontSize: 12,
    fontWeight: "700",
  },
  overrideSection: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    borderTopWidth: 1,
    borderTopColor: "rgba(150, 150, 150, 0.15)",
    paddingTop: 12,
  },
  overrideLabel: {
    fontSize: 12,
    flex: 1,
  },
  overrideInput: {
    width: 90,
    height: 38,
    borderRadius: 8,
    textAlign: "center",
    fontWeight: "700",
    fontSize: 14,
  },
  finishBtn: {
    height: 52,
    borderRadius: 16,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 10,
  },
  finishBtnText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
});
