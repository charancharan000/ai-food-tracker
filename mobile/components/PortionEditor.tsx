import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../hooks/useTheme";
import { FoodItemDetection } from "../types/food";
import { PORTION_PRESETS, scaleFoodItemNutrition } from "../utils/nutrition";

interface PortionEditorProps {
  item: FoodItemDetection;
  originalItem: FoodItemDetection;
  onChange: (updatedItem: FoodItemDetection) => void;
}

export const PortionEditor: React.FC<PortionEditorProps> = ({
  item,
  originalItem,
  onChange,
}) => {
  const { colors } = useTheme();

  const handleWeightChange = (deltaGrams: number) => {
    const currentWeight = item.estimated_weight_g || 100;
    const newWeight = Math.max(10, currentWeight + deltaGrams);
    const updated = scaleFoodItemNutrition(originalItem, newWeight, item.servings);
    onChange(updated);
  };

  const handleServingsChange = (deltaServings: number) => {
    const currentServings = item.servings || 1;
    const newServings = Math.max(0.2, Number((currentServings + deltaServings).toFixed(1)));
    const updated = scaleFoodItemNutrition(originalItem, item.estimated_weight_g, newServings);
    onChange(updated);
  };

  const handlePresetSelect = (multiplier: number) => {
    const baseWeight = originalItem.estimated_weight_g || 100;
    const targetWeight = Math.round(baseWeight * multiplier);
    const updated = scaleFoodItemNutrition(originalItem, targetWeight, 1.0);
    onChange(updated);
  };

  return (
    <View
      style={[
        styles.container,
        {
          backgroundColor: colors.surfaceLight,
          borderColor: colors.border,
        },
      ]}
    >
      <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>
        FINE-TUNE PORTION
      </Text>

      <View style={styles.presetsRow}>
        {PORTION_PRESETS.map((preset) => {
          const baseWeight = originalItem.estimated_weight_g || 100;
          const targetWeight = Math.round(baseWeight * preset.multiplier);
          const isSelected = Math.abs(item.estimated_weight_g - targetWeight) < 5;

          return (
            <TouchableOpacity
              key={preset.label}
              style={[
                styles.presetButton,
                {
                  backgroundColor: isSelected ? colors.primary : colors.surfaceHighlight,
                  borderColor: isSelected ? colors.primary : colors.border,
                },
              ]}
              onPress={() => handlePresetSelect(preset.multiplier)}
              activeOpacity={0.7}
            >
              <Text
                style={[
                  styles.presetText,
                  { color: isSelected ? "#FFFFFF" : colors.text },
                ]}
              >
                {preset.label}
              </Text>
              <Text
                style={[
                  styles.presetSubtext,
                  { color: isSelected ? "rgba(255,255,255,0.8)" : colors.textSecondary },
                ]}
              >
                {targetWeight}g
              </Text>
            </TouchableOpacity>
          );
        })}
      </View>

      <View style={styles.stepperSection}>
        <Text style={[styles.controlLabel, { color: colors.text }]}>Weight (grams)</Text>
        <View style={styles.stepperRow}>
          <TouchableOpacity
            style={[styles.stepBtn, { backgroundColor: colors.surfaceHighlight }]}
            onPress={() => handleWeightChange(-25)}
            activeOpacity={0.7}
          >
            <Ionicons name="remove" size={18} color={colors.text} />
          </TouchableOpacity>

          <View style={[styles.valueBox, { backgroundColor: colors.surface, borderColor: colors.border }]}>
            <Text style={[styles.valueText, { color: colors.text }]}>
              {Math.round(item.estimated_weight_g)} g
            </Text>
          </View>

          <TouchableOpacity
            style={[styles.stepBtn, { backgroundColor: colors.surfaceHighlight }]}
            onPress={() => handleWeightChange(25)}
            activeOpacity={0.7}
          >
            <Ionicons name="add" size={18} color={colors.text} />
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.stepperSection}>
        <Text style={[styles.controlLabel, { color: colors.text }]}>Servings</Text>
        <View style={styles.stepperRow}>
          <TouchableOpacity
            style={[styles.stepBtn, { backgroundColor: colors.surfaceHighlight }]}
            onPress={() => handleServingsChange(-0.5)}
            activeOpacity={0.7}
          >
            <Ionicons name="remove" size={18} color={colors.text} />
          </TouchableOpacity>

          <View style={[styles.valueBox, { backgroundColor: colors.surface, borderColor: colors.border }]}>
            <Text style={[styles.valueText, { color: colors.text }]}>
              {item.servings?.toFixed(1) || "1.0"}x
            </Text>
          </View>

          <TouchableOpacity
            style={[styles.stepBtn, { backgroundColor: colors.surfaceHighlight }]}
            onPress={() => handleServingsChange(0.5)}
            activeOpacity={0.7}
          >
            <Ionicons name="add" size={18} color={colors.text} />
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 18,
    padding: 16,
    borderWidth: 1,
    marginVertical: 12,
  },
  sectionTitle: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.8,
    marginBottom: 12,
  },
  presetsRow: {
    flexDirection: "row",
    gap: 8,
    marginBottom: 16,
  },
  presetButton: {
    flex: 1,
    paddingVertical: 8,
    borderRadius: 12,
    borderWidth: 1,
    alignItems: "center",
  },
  presetText: {
    fontSize: 12,
    fontWeight: "800",
  },
  presetSubtext: {
    fontSize: 10,
    fontWeight: "600",
    marginTop: 2,
  },
  stepperSection: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },
  controlLabel: {
    fontSize: 14,
    fontWeight: "600",
  },
  stepperRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  stepBtn: {
    width: 36,
    height: 36,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
  },
  valueBox: {
    minWidth: 84,
    paddingVertical: 7,
    paddingHorizontal: 12,
    borderRadius: 10,
    borderWidth: 1,
    alignItems: "center",
  },
  valueText: {
    fontSize: 15,
    fontWeight: "800",
  },
});
