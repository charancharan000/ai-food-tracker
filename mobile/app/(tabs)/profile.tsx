import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
  ActivityIndicator,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useAuth } from "../../hooks/useAuth";
import { useTheme } from "../../hooks/useTheme";
import { profileService } from "../../services/profileService";
import { storage } from "../../utils/storage";

export default function ProfileScreen() {
  const { user, logout, setUserState } = useAuth();
  const { colors, isDark, toggleTheme, palette, presets, setPalette, setThemeMode } = useTheme();
  const router = useRouter();

  const [isEditingGoals, setIsEditingGoals] = useState(false);
  const [calorieTarget, setCalorieTarget] = useState("");
  const [proteinTarget, setProteinTarget] = useState("");
  const [carbTarget, setCarbTarget] = useState("");
  const [fatTarget, setFatTarget] = useState("");
  const [waterTarget, setWaterTarget] = useState("");

  const [apiUrl, setApiUrl] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (user) {
      setCalorieTarget(String(Math.round(user.daily_calorie_target || 2000)));
      setProteinTarget(String(Math.round(user.protein_target || 150)));
      setCarbTarget(String(Math.round(user.carb_target || 250)));
      setFatTarget(String(Math.round(user.fat_target || 65)));
      setWaterTarget(String(user.daily_water_target_ml || 2500));
    }
    storage.getApiUrl().then(setApiUrl);
  }, [user]);

  const handleSaveGoals = async () => {
    try {
      setIsSaving(true);
      const updated = await profileService.updateGoals({
        daily_calorie_target: parseFloat(calorieTarget) || 2000,
        protein_target: parseFloat(proteinTarget) || 150,
        carb_target: parseFloat(carbTarget) || 250,
        fat_target: parseFloat(fatTarget) || 65,
        daily_water_target_ml: parseInt(waterTarget, 10) || 2500,
      });
      setUserState(updated);
      setIsEditingGoals(false);
      Alert.alert("Success", "Daily nutrition targets updated.");
    } catch {
      Alert.alert("Error", "Failed to update goals.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleSaveApiUrl = async () => {
    if (!apiUrl.trim()) return;
    await storage.setApiUrl(apiUrl.trim());
    Alert.alert("API URL Saved", `Target backend set to:\n${apiUrl.trim()}`);
  };

  const handleLogout = () => {
    Alert.alert("Log Out", "Are you sure you want to log out of NutriScan AI?", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Log Out",
        style: "destructive",
        onPress: async () => {
          await logout();
          router.replace("/(auth)/login");
        },
      },
    ]);
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      <View style={styles.topBar}>
        <Text style={[styles.headerTitle, { color: colors.text }]}>Profile</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <View style={styles.profileHeader}>
            <View style={[styles.avatarCircle, { backgroundColor: `${colors.primary}20` }]}>
              <Text style={[styles.avatarInitial, { color: colors.primary }]}>
                {user?.name ? user.name.charAt(0).toUpperCase() : "U"}
              </Text>
            </View>
            <View style={styles.profileInfo}>
              <Text style={[styles.userName, { color: colors.text }]}>{user?.name || "User"}</Text>
              <Text style={[styles.userEmail, { color: colors.textSecondary }]}>{user?.email}</Text>
              <View style={[styles.goalPill, { backgroundColor: `${colors.primary}15` }]}>
                <Text style={[styles.goalPillText, { color: colors.primary }]}>
                  Goal: {user?.goal ? user.goal.toUpperCase() : "MAINTAIN"}
                </Text>
              </View>
            </View>
          </View>

          <View style={[styles.bioStrip, { borderTopColor: colors.surfaceHighlight }]}>
            <View style={styles.bioCol}>
              <Text style={[styles.bioVal, { color: colors.text }]}>{user?.age || "--"}</Text>
              <Text style={[styles.bioLbl, { color: colors.textMuted }]}>Age</Text>
            </View>
            <View style={styles.bioCol}>
              <Text style={[styles.bioVal, { color: colors.text }]}>{user?.weight_kg || "--"} kg</Text>
              <Text style={[styles.bioLbl, { color: colors.textMuted }]}>Weight</Text>
            </View>
            <View style={styles.bioCol}>
              <Text style={[styles.bioVal, { color: colors.text }]}>{user?.height_cm || "--"} cm</Text>
              <Text style={[styles.bioLbl, { color: colors.textMuted }]}>Height</Text>
            </View>
            <View style={styles.bioCol}>
              <Text style={[styles.bioVal, { color: colors.text }]}>
                {user?.gender ? user.gender.slice(0, 1).toUpperCase() : "--"}
              </Text>
              <Text style={[styles.bioLbl, { color: colors.textMuted }]}>Gender</Text>
            </View>
          </View>
        </View>

        <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <View style={styles.cardTitleRow}>
            <View style={{ flexDirection: "row", alignItems: "center", gap: 8 }}>
              <Ionicons name="flag-outline" size={20} color={colors.primary} />
              <Text style={[styles.cardTitle, { color: colors.text }]}>Daily Nutrition Targets</Text>
            </View>

            <TouchableOpacity
              onPress={() => setIsEditingGoals(!isEditingGoals)}
              style={styles.editBtn}
            >
              <Text style={[styles.editBtnText, { color: colors.primary }]}>
                {isEditingGoals ? "Cancel" : "Edit"}
              </Text>
            </TouchableOpacity>
          </View>

          {isEditingGoals ? (
            <View style={styles.goalsForm}>
              <View style={styles.goalInputRow}>
                <Text style={[styles.goalLabel, { color: colors.textSecondary }]}>Daily Calories (kcal)</Text>
                <TextInput
                  style={[styles.goalInput, { backgroundColor: colors.surfaceHighlight, color: colors.text }]}
                  keyboardType="numeric"
                  value={calorieTarget}
                  onChangeText={setCalorieTarget}
                />
              </View>

              <View style={styles.goalInputRow}>
                <Text style={[styles.goalLabel, { color: colors.indigo }]}>Protein Target (g)</Text>
                <TextInput
                  style={[styles.goalInput, { backgroundColor: colors.surfaceHighlight, color: colors.text }]}
                  keyboardType="numeric"
                  value={proteinTarget}
                  onChangeText={setProteinTarget}
                />
              </View>

              <View style={styles.goalInputRow}>
                <Text style={[styles.goalLabel, { color: colors.amber }]}>Carb Target (g)</Text>
                <TextInput
                  style={[styles.goalInput, { backgroundColor: colors.surfaceHighlight, color: colors.text }]}
                  keyboardType="numeric"
                  value={carbTarget}
                  onChangeText={setCarbTarget}
                />
              </View>

              <View style={styles.goalInputRow}>
                <Text style={[styles.goalLabel, { color: colors.rose }]}>Fat Target (g)</Text>
                <TextInput
                  style={[styles.goalInput, { backgroundColor: colors.surfaceHighlight, color: colors.text }]}
                  keyboardType="numeric"
                  value={fatTarget}
                  onChangeText={setFatTarget}
                />
              </View>

              <View style={styles.goalInputRow}>
                <Text style={[styles.goalLabel, { color: colors.cyan }]}>Water Target (ml)</Text>
                <TextInput
                  style={[styles.goalInput, { backgroundColor: colors.surfaceHighlight, color: colors.text }]}
                  keyboardType="numeric"
                  value={waterTarget}
                  onChangeText={setWaterTarget}
                />
              </View>

              <TouchableOpacity
                style={[styles.saveGoalsBtn, { backgroundColor: colors.primary }]}
                onPress={handleSaveGoals}
                disabled={isSaving}
              >
                {isSaving ? (
                  <ActivityIndicator color="#FFFFFF" />
                ) : (
                  <Text style={styles.saveGoalsBtnText}>Save Targets</Text>
                )}
              </TouchableOpacity>
            </View>
          ) : (
            <View style={styles.goalsDisplay}>
              <View style={styles.goalDisplayItem}>
                <Text style={[styles.goalDisplayNum, { color: colors.primary }]}>
                  {Math.round(user?.daily_calorie_target || 2000)}
                </Text>
                <Text style={[styles.goalDisplayLbl, { color: colors.textSecondary }]}>Calories / day</Text>
              </View>

              <View style={styles.goalDisplayItem}>
                <Text style={[styles.goalDisplayNum, { color: colors.indigo }]}>
                  {Math.round(user?.protein_target || 150)}g
                </Text>
                <Text style={[styles.goalDisplayLbl, { color: colors.textSecondary }]}>Protein</Text>
              </View>

              <View style={styles.goalDisplayItem}>
                <Text style={[styles.goalDisplayNum, { color: colors.amber }]}>
                  {Math.round(user?.carb_target || 250)}g
                </Text>
                <Text style={[styles.goalDisplayLbl, { color: colors.textSecondary }]}>Carbs</Text>
              </View>

              <View style={styles.goalDisplayItem}>
                <Text style={[styles.goalDisplayNum, { color: colors.rose }]}>
                  {Math.round(user?.fat_target || 65)}g
                </Text>
                <Text style={[styles.goalDisplayLbl, { color: colors.textSecondary }]}>Fat</Text>
              </View>
            </View>
          )}
        </View>

        <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Text style={[styles.cardTitle, { color: colors.text, marginBottom: 12 }]}>Settings</Text>

          <View style={styles.themeStudio}>
            <View style={styles.themeHeaderRow}>
              <View style={styles.settingsRowLeft}>
                <Ionicons
                  name={isDark ? "moon-outline" : "sunny-outline"}
                  size={20}
                  color={colors.primary}
                />
                <Text style={[styles.settingsRowLabel, { color: colors.text }]}>Theme</Text>
              </View>

              <View style={[styles.modeTogglePills, { backgroundColor: colors.surfaceHighlight }]}>
                <TouchableOpacity
                  style={[
                    styles.modePill,
                    isDark && { backgroundColor: colors.primary },
                  ]}
                  onPress={() => setThemeMode("dark")}
                  activeOpacity={0.7}
                >
                  <Ionicons name="moon" size={13} color={isDark ? "#FFFFFF" : colors.textMuted} />
                  <Text style={[styles.modePillText, { color: isDark ? "#FFFFFF" : colors.textMuted }]}>
                    Dark
                  </Text>
                </TouchableOpacity>

                <TouchableOpacity
                  style={[
                    styles.modePill,
                    !isDark && { backgroundColor: colors.primary },
                  ]}
                  onPress={() => setThemeMode("light")}
                  activeOpacity={0.7}
                >
                  <Ionicons name="sunny" size={13} color={!isDark ? "#FFFFFF" : colors.textMuted} />
                  <Text style={[styles.modePillText, { color: !isDark ? "#FFFFFF" : colors.textMuted }]}>
                    Light
                  </Text>
                </TouchableOpacity>
              </View>
            </View>

            <Text style={[styles.paletteLabel, { color: colors.textSecondary }]}>ACCENT COLOR</Text>
            <View style={styles.paletteGrid}>
              {presets.map((preset) => {
                const isSelected = palette === preset.id;
                return (
                  <TouchableOpacity
                    key={preset.id}
                    style={[
                      styles.paletteCard,
                      {
                        backgroundColor: isSelected ? `${preset.accent}15` : colors.surfaceLight,
                        borderColor: isSelected ? preset.accent : colors.border,
                      },
                    ]}
                    onPress={() => setPalette(preset.id)}
                    activeOpacity={0.7}
                  >
                    <View style={styles.paletteTop}>
                      <View style={[styles.colorDot, { backgroundColor: preset.accent }]} />
                      {isSelected && (
                        <Ionicons name="checkmark-circle" size={16} color={preset.accent} />
                      )}
                    </View>
                    <Text
                      style={[
                        styles.paletteName,
                        { color: isSelected ? preset.accent : colors.text },
                      ]}
                    >
                      {preset.name}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>
          </View>

          <View style={[styles.apiConfigBox, { borderTopColor: colors.surfaceHighlight }]}>
            <Text style={[styles.apiConfigTitle, { color: colors.textSecondary }]}>
              API SERVER URL
            </Text>
            <View style={styles.apiInputRow}>
              <TextInput
                style={[styles.apiInput, { backgroundColor: colors.surfaceHighlight, color: colors.text }]}
                value={apiUrl}
                onChangeText={setApiUrl}
                placeholder="http://localhost:8000/api/v1"
                placeholderTextColor={colors.textMuted}
                autoCapitalize="none"
              />
              <TouchableOpacity
                style={[styles.apiSaveBtn, { backgroundColor: colors.primary }]}
                onPress={handleSaveApiUrl}
              >
                <Text style={styles.apiSaveBtnText}>Save</Text>
              </TouchableOpacity>
            </View>
            <Text style={[styles.apiHint, { color: colors.textMuted }]}>
              Use 10.0.2.2:8000 for Android emulator or your local LAN IP for physical device testing.
            </Text>
          </View>
        </View>

        <TouchableOpacity
          style={[styles.logoutBtn, { borderColor: colors.danger }]}
          onPress={handleLogout}
          activeOpacity={0.7}
        >
          <Ionicons name="log-out-outline" size={20} color={colors.danger} />
          <Text style={[styles.logoutBtnText, { color: colors.danger }]}>Log Out</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  topBar: {
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: "800",
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 40,
    gap: 16,
  },
  card: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 18,
  },
  profileHeader: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 16,
  },
  avatarCircle: {
    width: 60,
    height: 60,
    borderRadius: 30,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 14,
  },
  avatarInitial: {
    fontSize: 26,
    fontWeight: "800",
  },
  profileInfo: {
    flex: 1,
  },
  userName: {
    fontSize: 18,
    fontWeight: "800",
    marginBottom: 2,
  },
  userEmail: {
    fontSize: 13,
    marginBottom: 6,
  },
  goalPill: {
    alignSelf: "flex-start",
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 8,
  },
  goalPillText: {
    fontSize: 11,
    fontWeight: "700",
  },
  bioStrip: {
    flexDirection: "row",
    borderTopWidth: 1,
    paddingTop: 14,
  },
  bioCol: {
    flex: 1,
    alignItems: "center",
  },
  bioVal: {
    fontSize: 16,
    fontWeight: "700",
  },
  bioLbl: {
    fontSize: 11,
    marginTop: 2,
  },
  cardTitleRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 14,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: "700",
  },
  editBtn: {
    padding: 4,
  },
  editBtnText: {
    fontSize: 14,
    fontWeight: "700",
  },
  goalsDisplay: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  goalDisplayItem: {
    alignItems: "center",
    flex: 1,
  },
  goalDisplayNum: {
    fontSize: 20,
    fontWeight: "800",
  },
  goalDisplayLbl: {
    fontSize: 11,
    marginTop: 2,
  },
  goalsForm: {
    gap: 10,
  },
  goalInputRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  goalLabel: {
    fontSize: 13,
    fontWeight: "600",
  },
  goalInput: {
    width: 90,
    height: 38,
    borderRadius: 8,
    textAlign: "center",
    fontWeight: "700",
    fontSize: 14,
  },
  saveGoalsBtn: {
    height: 44,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 8,
  },
  saveGoalsBtnText: {
    color: "#FFFFFF",
    fontSize: 14,
    fontWeight: "700",
  },
  themeStudio: {
    paddingVertical: 4,
    marginBottom: 8,
  },
  themeHeaderRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 14,
  },
  settingsRowLeft: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  settingsRowLabel: {
    fontSize: 14,
    fontWeight: "700",
  },
  modeTogglePills: {
    flexDirection: "row",
    borderRadius: 20,
    padding: 3,
  },
  modePill: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 16,
  },
  modePillText: {
    fontSize: 12,
    fontWeight: "700",
  },
  paletteLabel: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
    marginBottom: 10,
  },
  paletteGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 10,
  },
  paletteCard: {
    width: "48%",
    borderRadius: 14,
    borderWidth: 1.5,
    padding: 12,
  },
  paletteTop: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  colorDot: {
    width: 14,
    height: 14,
    borderRadius: 7,
  },
  paletteName: {
    fontSize: 13,
    fontWeight: "700",
  },
  apiConfigBox: {
    borderTopWidth: 1,
    paddingTop: 14,
    marginTop: 6,
  },
  apiConfigTitle: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
    marginBottom: 8,
  },
  apiInputRow: {
    flexDirection: "row",
    gap: 8,
  },
  apiInput: {
    flex: 1,
    height: 40,
    borderRadius: 10,
    paddingHorizontal: 12,
    fontSize: 13,
  },
  apiSaveBtn: {
    paddingHorizontal: 14,
    height: 40,
    borderRadius: 10,
    alignItems: "center",
    justifyContent: "center",
  },
  apiSaveBtnText: {
    color: "#FFFFFF",
    fontSize: 13,
    fontWeight: "700",
  },
  apiHint: {
    fontSize: 11,
    marginTop: 6,
    lineHeight: 16,
  },
  logoutBtn: {
    height: 50,
    borderRadius: 14,
    borderWidth: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    marginTop: 8,
  },
  logoutBtnText: {
    fontSize: 15,
    fontWeight: "700",
  },
});
