import React, { useState, useEffect, useRef } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
  Alert,
  ActivityIndicator,
  Animated,
  Easing,
  TextInput,
} from "react-native";
import { useRouter, useLocalSearchParams } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import * as ImagePicker from "expo-image-picker";
import { useTheme } from "../../hooks/useTheme";
import { foodService } from "../../services/foodService";
import { FoodAnalysisResponse, FoodItemDetection, MealType } from "../../types/food";
import { calculateTotals, scaleFoodItemNutrition } from "../../utils/nutrition";
import { AnalysisLoadingModal } from "../../components/AnalysisLoadingModal";
import { FoodItemCard } from "../../components/FoodItemCard";
import { NutritionSummaryBar } from "../../components/NutritionSummaryBar";

const POPULAR_TRAINED_DISHES = [
  { label: "Auto Detect", value: "" },
  { label: "🍗 Chicken Biryani", value: "biryani" },
  { label: "🍕 Pepperoni Pizza", value: "pizza" },
  { label: "🍔 Cheeseburger & Fries", value: "burger" },
  { label: "🥞 Masala Dosa", value: "dosa" },
  { label: "🥩 Grilled Chicken & Rice", value: "grilled chicken" },
  { label: "🐟 Salmon & Quinoa", value: "salmon" },
  { label: "🥘 Paneer Butter Masala", value: "paneer" },
  { label: "🍛 Chicken Curry & Rice", value: "chicken curry" },
  { label: "🍝 Spaghetti Bolognese", value: "pasta" },
  { label: "🥑 Avocado Toast & Eggs", value: "avocado toast" },
  { label: "🥗 Caesar Salad", value: "caesar salad" },
  { label: "🍣 Sushi Platter", value: "sushi" },
  { label: "🥩 Ribeye Steak & Potatoes", value: "steak" },
  { label: "🥣 Oatmeal & Berries", value: "oatmeal" },
  { label: "🍉 Fresh Fruit Medley", value: "fruit" },
];

export default function FoodScannerScreen() {
  const { colors } = useTheme();
  const router = useRouter();
  const params = useLocalSearchParams<{ preferredMealType?: string }>();

  const [step, setStep] = useState<"idle" | "preview" | "result">("idle");
  const [selectedImageUri, setSelectedImageUri] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const [selectedDishHint, setSelectedDishHint] = useState<string>("");
  const [customDishText, setCustomDishText] = useState<string>("");

  const [detectedItems, setDetectedItems] = useState<FoodItemDetection[]>([]);
  const [originalItems, setOriginalItems] = useState<FoodItemDetection[]>([]);
  const [notes, setNotes] = useState<string>("");
  const [selectedMealType, setSelectedMealType] = useState<MealType>(
    (params.preferredMealType as MealType) || "Lunch"
  );
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const scanLineAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (step === "idle") {
      const loopAnim = Animated.loop(
        Animated.sequence([
          Animated.timing(scanLineAnim, {
            toValue: 190,
            duration: 1700,
            easing: Easing.inOut(Easing.quad),
            useNativeDriver: true,
          }),
          Animated.timing(scanLineAnim, {
            toValue: 0,
            duration: 1700,
            easing: Easing.inOut(Easing.quad),
            useNativeDriver: true,
          }),
        ])
      );
      loopAnim.start();
      return () => loopAnim.stop();
    }
  }, [step]);

  const handleTakePhoto = async () => {
    try {
      const permission = await ImagePicker.requestCameraPermissionsAsync();
      if (!permission.granted) {
        Alert.alert(
          "Camera Permission Required",
          "Please grant camera access to scan your meals with AI."
        );
        return;
      }

      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ["images"],
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0].uri) {
        setSelectedImageUri(result.assets[0].uri);
        setStep("preview");
        setErrorMessage(null);
      }
    } catch (e) {
      console.error("Camera error:", e);
      Alert.alert("Error", "Could not open camera. Please try selecting from gallery.");
    }
  };

  const handlePickFromGallery = async () => {
    try {
      const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (!permission.granted) {
        Alert.alert(
          "Gallery Permission Required",
          "Please grant photo library access to upload meal pictures."
        );
        return;
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ["images"],
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });

      if (!result.canceled && result.assets[0].uri) {
        setSelectedImageUri(result.assets[0].uri);
        setStep("preview");
        setErrorMessage(null);
      }
    } catch (e) {
      console.error("Gallery error:", e);
      Alert.alert("Error", "Could not open photo gallery.");
    }
  };

  const handleAnalyzeFood = async () => {
    if (!selectedImageUri) return;

    try {
      setIsAnalyzing(true);
      setErrorMessage(null);

      const effectiveHint = customDishText.trim() || selectedDishHint;

      const analysis: FoodAnalysisResponse = await foodService.analyzeFood(
        selectedImageUri,
        "image/jpeg",
        effectiveHint || undefined
      );

      if (!analysis.food_items || analysis.food_items.length === 0) {
        throw new Error("No food items detected in photo.");
      }

      setDetectedItems(analysis.food_items);
      setOriginalItems(JSON.parse(JSON.stringify(analysis.food_items)));
      setNotes(analysis.notes || "");
      setStep("result");
    } catch (e: any) {
      const err =
        e.response?.data?.detail ||
        "Unable to analyze this image. Please try another clear food photo.";
      setErrorMessage(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleUpdateItem = (index: number, updatedItem: FoodItemDetection) => {
    const next = [...detectedItems];
    next[index] = updatedItem;
    setDetectedItems(next);
  };

  const handleRemoveItem = (index: number) => {
    if (detectedItems.length === 1) {
      Alert.alert(
        "Remove Item",
        "A meal must have at least one food item. Would you like to retake or cancel?",
        [
          { text: "Cancel", style: "cancel" },
          { text: "Retake Photo", onPress: handleResetScanner },
        ]
      );
      return;
    }

    const nextDetected = detectedItems.filter((_, i) => i !== index);
    const nextOriginal = originalItems.filter((_, i) => i !== index);
    setDetectedItems(nextDetected);
    setOriginalItems(nextOriginal);
  };

  const handleResetScanner = () => {
    setSelectedImageUri(null);
    setDetectedItems([]);
    setOriginalItems([]);
    setSelectedDishHint("");
    setCustomDishText("");
    setErrorMessage(null);
    setStep("idle");
  };

  const handleSaveMeal = async () => {
    if (detectedItems.length === 0) return;

    try {
      setIsSaving(true);
      await foodService.createMeal({
        meal_type: selectedMealType,
        notes: notes,
        food_items: detectedItems.map((item) => ({
          name: item.name,
          estimated_weight_g: item.estimated_weight_g,
          servings: item.servings,
          calories: item.calories,
          protein_g: item.protein_g,
          carbs_g: item.carbs_g,
          fat_g: item.fat_g,
          fiber_g: item.fiber_g,
          sugar_g: item.sugar_g,
          sodium_mg: item.sodium_mg,
          confidence: item.confidence,
        })),
      });

      Alert.alert(
        "Meal Logged! 🎉",
        `Your ${selectedMealType.toLowerCase()} has been added to today's food log.`,
        [
          {
            text: "View Dashboard",
            onPress: () => {
              handleResetScanner();
              router.replace("/(tabs)");
            },
          },
          {
            text: "Log Another",
            onPress: handleResetScanner,
          },
        ]
      );
    } catch (e: any) {
      const err = e.response?.data?.detail || "Failed to save meal. Please try again.";
      Alert.alert("Save Error", err);
    } finally {
      setIsSaving(false);
    }
  };

  const calculatedTotals = calculateTotals(detectedItems);

  const avgConfidence = detectedItems.length > 0
    ? Math.round((detectedItems.reduce((acc, i) => acc + (i.confidence || 0.8), 0) / detectedItems.length) * 100)
    : 85;

  const mealTypesList: MealType[] = ["Breakfast", "Lunch", "Snack", "Dinner"];

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      <View style={styles.topBar}>
        {step !== "idle" ? (
          <TouchableOpacity onPress={handleResetScanner} style={styles.headerIconBtn}>
            <Ionicons name="arrow-back" size={24} color={colors.text} />
          </TouchableOpacity>
        ) : (
          <View style={{ width: 36 }} />
        )}
        <Text style={[styles.headerTitle, { color: colors.text }]}>
          {step === "idle" && "Scan Meal"}
          {step === "preview" && "Preview Photo"}
          {step === "result" && "Meal Details"}
        </Text>
        <View style={{ width: 36 }} />
      </View>

      <AnalysisLoadingModal visible={isAnalyzing} />

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {errorMessage && (
          <View style={[styles.errorCard, { backgroundColor: `${colors.danger}15`, borderColor: colors.danger }]}>
            <Ionicons name="alert-circle" size={22} color={colors.danger} />
            <Text style={[styles.errorCardText, { color: colors.danger }]}>{errorMessage}</Text>
          </View>
        )}

        {step === "idle" && (
          <View style={styles.idleContainer}>
            <View style={[styles.viewfinder, { backgroundColor: colors.surface, borderColor: colors.border }]}>
              <View style={[styles.scannerCorner, styles.cornerTL, { borderColor: colors.primary }]} />
              <View style={[styles.scannerCorner, styles.cornerTR, { borderColor: colors.primary }]} />
              <View style={[styles.scannerCorner, styles.cornerBL, { borderColor: colors.primary }]} />
              <View style={[styles.scannerCorner, styles.cornerBR, { borderColor: colors.primary }]} />

              <Animated.View
                style={[
                  styles.laserLine,
                  {
                    backgroundColor: colors.primary,
                    shadowColor: colors.primary,
                    transform: [{ translateY: scanLineAnim }],
                  },
                ]}
              />

              <View style={[styles.centerScanIcon, { backgroundColor: `${colors.primary}15` }]}>
                <Ionicons name="scan-outline" size={54} color={colors.primary} />
              </View>
              <Text style={[styles.scanPrompt, { color: colors.text }]}>
                Take or upload photo
              </Text>
              <Text style={[styles.scanHelp, { color: colors.textSecondary }]}>
                Hold camera directly over the plate or bowl for best results
              </Text>
            </View>

            <View style={styles.actionButtonsCol}>
              <TouchableOpacity
                style={[styles.primaryActionBtn, { backgroundColor: colors.primary }]}
                onPress={handleTakePhoto}
                activeOpacity={0.8}
              >
                <Ionicons name="camera" size={22} color="#FFFFFF" />
                <Text style={styles.primaryActionBtnText}>Take Photo</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[
                  styles.secondaryActionBtn,
                  { backgroundColor: colors.surface, borderColor: colors.border },
                ]}
                onPress={handlePickFromGallery}
                activeOpacity={0.7}
              >
                <Ionicons name="images-outline" size={22} color={colors.primary} />
                <Text style={[styles.secondaryActionBtnText, { color: colors.text }]}>
                  Upload from Gallery
                </Text>
              </TouchableOpacity>
            </View>

            <View style={[styles.tipsBox, { backgroundColor: colors.surfaceLight, borderColor: colors.border }]}>
              <View style={styles.tipsHeader}>
                <Ionicons name="bulb-outline" size={18} color={colors.amber} />
                <Text style={[styles.tipsTitle, { color: colors.text }]}>Tips</Text>
              </View>
              <Text style={[styles.tipsText, { color: colors.textSecondary }]}>
                • Good lighting and visible portions improve accuracy{"\n"}
                • Mixed plates with multiple items are recognized separately{"\n"}
                • You can fine-tune portion weights before saving
              </Text>
            </View>
          </View>
        )}

        {step === "preview" && selectedImageUri && (
          <View style={styles.previewContainer}>
            <View style={[styles.imageCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
              <Image source={{ uri: selectedImageUri }} style={styles.previewImage} resizeMode="cover" />
            </View>

            <View style={styles.modelBadgeRow}>
              <View style={[styles.aiModelBadge, { backgroundColor: `${colors.primary}15`, borderColor: colors.primary }]}>
                <Ionicons name="sparkles" size={14} color={colors.primary} />
                <Text style={[styles.aiModelBadgeText, { color: colors.primary }]}>
                  AI Multi-Image Vision Engine v2.0
                </Text>
              </View>
            </View>

            <Text style={[styles.previewHeading, { color: colors.text }]}>
              {customDishText || selectedDishHint ? "Custom Dish Selected" : "Ready to Analyze"}
            </Text>
            <Text style={[styles.previewSubheading, { color: colors.textSecondary }]}>
              Trained on multi-image food datasets for accurate portion recognition and macronutrient breakdown.
            </Text>

            <View style={styles.chipSection}>
              <Text style={[styles.chipSectionLabel, { color: colors.textSecondary }]}>
                POPULAR DISH MATCH (OPTIONAL)
              </Text>
              <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chipsScroll}>
                {POPULAR_TRAINED_DISHES.map((d) => {
                  const isSelected = selectedDishHint === d.value && !customDishText;
                  return (
                    <TouchableOpacity
                      key={d.label}
                      style={[
                        styles.dishChip,
                        {
                          backgroundColor: isSelected ? colors.primary : colors.surface,
                          borderColor: isSelected ? colors.primary : colors.border,
                        },
                      ]}
                      onPress={() => {
                        setSelectedDishHint(d.value);
                        setCustomDishText("");
                      }}
                      activeOpacity={0.7}
                    >
                      <Text
                        style={[
                          styles.dishChipText,
                          { color: isSelected ? "#FFFFFF" : colors.text },
                        ]}
                      >
                        {d.label}
                      </Text>
                    </TouchableOpacity>
                  );
                })}
              </ScrollView>
            </View>

            <View style={[styles.customInputContainer, { backgroundColor: colors.surface, borderColor: colors.border }]}>
              <Ionicons name="search-outline" size={18} color={colors.textSecondary} style={{ marginRight: 8 }} />
              <TextInput
                style={[styles.customTextInput, { color: colors.text }]}
                placeholder="Or type dish (e.g. Biryani, Pizza, Dosa)..."
                placeholderTextColor={colors.textMuted}
                value={customDishText}
                onChangeText={(text) => {
                  setCustomDishText(text);
                  if (text) setSelectedDishHint("");
                }}
              />
              {customDishText ? (
                <TouchableOpacity onPress={() => setCustomDishText("")}>
                  <Ionicons name="close-circle" size={18} color={colors.textSecondary} />
                </TouchableOpacity>
              ) : null}
            </View>

            <View style={styles.previewActions}>
              <TouchableOpacity
                style={[styles.primaryActionBtn, { backgroundColor: colors.primary }]}
                onPress={handleAnalyzeFood}
                activeOpacity={0.8}
              >
                <Ionicons name="sparkles" size={20} color="#FFFFFF" />
                <Text style={styles.primaryActionBtnText}>
                  {customDishText || selectedDishHint ? "Analyze Selected Dish" : "Analyze Food with AI"}
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[styles.secondaryActionBtn, { backgroundColor: colors.surface, borderColor: colors.border }]}
                onPress={handleResetScanner}
                activeOpacity={0.7}
              >
                <Ionicons name="refresh" size={20} color={colors.textSecondary} />
                <Text style={[styles.secondaryActionBtnText, { color: colors.text }]}>
                  Retake Photo
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        {step === "result" && (
          <View style={styles.resultContainer}>
            <View style={[styles.resultBanner, { backgroundColor: colors.surface, borderColor: colors.border }]}>
              <View style={styles.resultTopRow}>
                <View>
                  <Text style={[styles.resultEyebrow, { color: colors.textSecondary }]}>
                    ITEMS DETECTED ({detectedItems.length})
                  </Text>
                  <Text style={[styles.resultTotalCals, { color: colors.primary }]}>
                    {Math.round(calculatedTotals.calories)}{" "}
                    <Text style={[styles.resultUnit, { color: colors.textSecondary }]}>kcal</Text>
                  </Text>
                </View>

                <View
                  style={[
                    styles.confidenceBadge,
                    {
                      backgroundColor:
                        avgConfidence >= 80 ? `${colors.emerald}20` : `${colors.amber}20`,
                    },
                  ]}
                >
                  <Ionicons
                    name="shield-checkmark"
                    size={16}
                    color={avgConfidence >= 80 ? colors.emerald : colors.amber}
                  />
                  <Text
                    style={[
                      styles.confidenceBadgeText,
                      { color: avgConfidence >= 80 ? colors.emerald : colors.amber },
                    ]}
                  >
                    {avgConfidence}% match
                  </Text>
                </View>
              </View>

              <NutritionSummaryBar total={calculatedTotals} />

              <Text style={[styles.disclaimer, { color: colors.textMuted }]}>
                Estimated values. Tap options on any item to adjust weight or servings.
              </Text>
            </View>

            <View style={styles.mealTypeSection}>
              <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>LOG AS MEAL TYPE</Text>
              <View style={styles.mealTypesRow}>
                {mealTypesList.map((type) => (
                  <TouchableOpacity
                    key={type}
                    style={[
                      styles.mealTypeChip,
                      {
                        backgroundColor:
                          selectedMealType === type ? colors.primary : colors.surface,
                        borderColor: selectedMealType === type ? colors.primary : colors.border,
                      },
                    ]}
                    onPress={() => setSelectedMealType(type)}
                    activeOpacity={0.7}
                  >
                    <Text
                      style={[
                        styles.mealTypeChipText,
                        { color: selectedMealType === type ? "#FFFFFF" : colors.text },
                      ]}
                    >
                      {type}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            <Text style={[styles.sectionTitle, { color: colors.textSecondary, marginTop: 10 }]}>
              DETECTED ITEMS & PORTIONS
            </Text>

            {detectedItems.map((item, index) => (
              <FoodItemCard
                key={`${item.name}-${index}`}
                item={item}
                originalItem={originalItems[index] || item}
                index={index}
                onUpdate={(updated) => handleUpdateItem(index, updated)}
                onRemove={() => handleRemoveItem(index)}
              />
            ))}

            {notes ? (
              <View style={[styles.notesCard, { backgroundColor: colors.surfaceLight, borderColor: colors.border }]}>
                <Ionicons name="information-circle-outline" size={18} color={colors.primary} />
                <Text style={[styles.notesText, { color: colors.textSecondary }]}>{notes}</Text>
              </View>
            ) : null}

            <TouchableOpacity
              style={[styles.saveMealBtn, { backgroundColor: colors.primary }]}
              onPress={handleSaveMeal}
              disabled={isSaving}
              activeOpacity={0.8}
            >
              {isSaving ? (
                <ActivityIndicator color="#FFFFFF" />
              ) : (
                <>
                  <Ionicons name="checkmark-done" size={22} color="#FFFFFF" />
                  <Text style={styles.saveMealBtnText}>
                    Add to Today's {selectedMealType} Log
                  </Text>
                </>
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.retakeBtn, { borderColor: colors.border }]}
              onPress={handleResetScanner}
              disabled={isSaving}
              activeOpacity={0.7}
            >
              <Text style={[styles.retakeBtnText, { color: colors.textSecondary }]}>
                Discard & Scan Another
              </Text>
            </TouchableOpacity>
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
  topBar: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  headerIconBtn: {
    width: 36,
    height: 36,
    justifyContent: "center",
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: "800",
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  errorCard: {
    flexDirection: "row",
    alignItems: "center",
    padding: 14,
    borderRadius: 14,
    borderWidth: 1,
    marginBottom: 16,
    gap: 10,
  },
  errorCardText: {
    fontSize: 13,
    fontWeight: "600",
    flex: 1,
  },
  idleContainer: {
    paddingTop: 10,
  },
  viewfinder: {
    height: 280,
    borderRadius: 24,
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
    position: "relative",
    marginBottom: 24,
    overflow: "hidden",
  },
  laserLine: {
    position: "absolute",
    top: 24,
    left: 24,
    right: 24,
    height: 3,
    borderRadius: 1.5,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.9,
    shadowRadius: 8,
    elevation: 4,
    zIndex: 10,
  },
  scannerCorner: {
    position: "absolute",
    width: 32,
    height: 32,
    borderWidth: 3,
  },
  cornerTL: { top: 16, left: 16, borderRightWidth: 0, borderBottomWidth: 0, borderTopLeftRadius: 10 },
  cornerTR: { top: 16, right: 16, borderLeftWidth: 0, borderBottomWidth: 0, borderTopRightRadius: 10 },
  cornerBL: { bottom: 16, left: 16, borderRightWidth: 0, borderTopWidth: 0, borderBottomLeftRadius: 10 },
  cornerBR: { bottom: 16, right: 16, borderLeftWidth: 0, borderTopWidth: 0, borderBottomRightRadius: 10 },
  centerScanIcon: {
    width: 90,
    height: 90,
    borderRadius: 45,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 16,
  },
  scanPrompt: {
    fontSize: 18,
    fontWeight: "800",
    textAlign: "center",
    marginBottom: 6,
  },
  scanHelp: {
    fontSize: 13,
    textAlign: "center",
    lineHeight: 18,
  },
  actionButtonsCol: {
    gap: 12,
    marginBottom: 24,
  },
  primaryActionBtn: {
    height: 54,
    borderRadius: 16,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
  },
  primaryActionBtnText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
  secondaryActionBtn: {
    height: 52,
    borderRadius: 16,
    borderWidth: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 10,
  },
  secondaryActionBtnText: {
    fontSize: 15,
    fontWeight: "700",
  },
  tipsBox: {
    padding: 16,
    borderRadius: 16,
    borderWidth: 1,
  },
  tipsHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    marginBottom: 8,
  },
  tipsTitle: {
    fontSize: 14,
    fontWeight: "700",
  },
  tipsText: {
    fontSize: 12,
    lineHeight: 18,
  },
  previewContainer: {
    paddingTop: 10,
  },
  imageCard: {
    height: 300,
    borderRadius: 20,
    overflow: "hidden",
    borderWidth: 1,
    marginBottom: 20,
  },
  previewImage: {
    width: "100%",
    height: "100%",
  },
  previewHeading: {
    fontSize: 20,
    fontWeight: "800",
    textAlign: "center",
    marginBottom: 6,
  },
  previewSubheading: {
    fontSize: 13,
    textAlign: "center",
    lineHeight: 18,
    marginBottom: 16,
  },
  modelBadgeRow: {
    alignItems: "center",
    marginBottom: 12,
  },
  aiModelBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    paddingHorizontal: 12,
    paddingVertical: 5,
    borderRadius: 20,
    borderWidth: 1,
  },
  aiModelBadgeText: {
    fontSize: 12,
    fontWeight: "700",
  },
  chipSection: {
    marginBottom: 14,
  },
  chipSectionLabel: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
    marginBottom: 8,
  },
  chipsScroll: {
    gap: 8,
    paddingVertical: 4,
  },
  dishChip: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
  },
  dishChipText: {
    fontSize: 13,
    fontWeight: "600",
  },
  customInputContainer: {
    flexDirection: "row",
    alignItems: "center",
    borderWidth: 1,
    borderRadius: 14,
    paddingHorizontal: 12,
    height: 46,
    marginBottom: 16,
  },
  customTextInput: {
    flex: 1,
    fontSize: 13,
    paddingVertical: 0,
  },
  previewActions: {
    gap: 12,
  },
  resultContainer: {
    paddingTop: 4,
  },
  resultBanner: {
    borderRadius: 22,
    borderWidth: 1,
    padding: 18,
    marginBottom: 16,
  },
  resultTopRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
  },
  resultEyebrow: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
  },
  resultTotalCals: {
    fontSize: 32,
    fontWeight: "900",
    marginTop: 2,
  },
  resultUnit: {
    fontSize: 16,
    fontWeight: "600",
  },
  confidenceBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
  },
  confidenceBadgeText: {
    fontSize: 12,
    fontWeight: "700",
  },
  disclaimer: {
    fontSize: 11,
    fontStyle: "italic",
    textAlign: "center",
  },
  mealTypeSection: {
    marginBottom: 14,
  },
  sectionTitle: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
    marginBottom: 8,
  },
  mealTypesRow: {
    flexDirection: "row",
    gap: 8,
  },
  mealTypeChip: {
    flex: 1,
    paddingVertical: 10,
    borderRadius: 12,
    borderWidth: 1,
    alignItems: "center",
  },
  mealTypeChipText: {
    fontSize: 12,
    fontWeight: "700",
  },
  notesCard: {
    flexDirection: "row",
    alignItems: "center",
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    gap: 8,
    marginVertical: 10,
  },
  notesText: {
    fontSize: 12,
    flex: 1,
    lineHeight: 16,
  },
  saveMealBtn: {
    height: 54,
    borderRadius: 16,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    marginTop: 14,
  },
  saveMealBtnText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
  retakeBtn: {
    height: 48,
    borderRadius: 14,
    borderWidth: 1,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 10,
  },
  retakeBtnText: {
    fontSize: 14,
    fontWeight: "600",
  },
});
