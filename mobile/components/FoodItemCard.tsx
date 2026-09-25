import React, { useState } from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../hooks/useTheme";
import { FoodItemDetection } from "../types/food";
import { PortionEditor } from "./PortionEditor";

interface FoodItemCardProps {
  item: FoodItemDetection;
  originalItem: FoodItemDetection;
  index: number;
  onUpdate: (updated: FoodItemDetection) => void;
  onRemove: () => void;
}

export const FoodItemCard: React.FC<FoodItemCardProps> = ({
  item,
  originalItem,
  index,
  onUpdate,
  onRemove,
}) => {
  const { colors } = useTheme();
  const [isEditing, setIsEditing] = useState(false);

  const confidencePct = Math.round((item.confidence || 0.8) * 100);
  const confidenceColor = confidencePct >= 80 ? colors.emerald : confidencePct >= 65 ? colors.amber : colors.rose;

  return (
    <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
      <View style={styles.headerRow}>
        <View style={styles.titleInfo}>
          <View style={[styles.indexBadge, { backgroundColor: colors.surfaceHighlight }]}>
            <Text style={[styles.indexText, { color: colors.primary }]}>{index + 1}</Text>
          </View>
          <View style={styles.nameContainer}>
            <Text style={[styles.foodName, { color: colors.text }]}>{item.name}</Text>
            <View style={styles.metaRow}>
              <Text style={[styles.portionSubtitle, { color: colors.textSecondary }]}>
                {Math.round(item.estimated_weight_g)} g • {Math.round(item.calories)} kcal
              </Text>
              <View style={[styles.confidencePill, { backgroundColor: `${confidenceColor}15` }]}>
                <Text style={[styles.confidenceText, { color: confidenceColor }]}>
                  {confidencePct}% match
                </Text>
              </View>
            </View>
          </View>
        </View>

        <View style={styles.actions}>
          <TouchableOpacity
            style={[styles.actionBtn, { backgroundColor: colors.surfaceHighlight }]}
            onPress={() => setIsEditing(!isEditing)}
            activeOpacity={0.7}
          >
            <Ionicons
              name={isEditing ? "chevron-up" : "options-outline"}
              size={18}
              color={isEditing ? colors.primary : colors.textSecondary}
            />
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.actionBtn, { backgroundColor: `${colors.danger}15` }]}
            onPress={onRemove}
            activeOpacity={0.7}
          >
            <Ionicons name="trash-outline" size={17} color={colors.danger} />
          </TouchableOpacity>
        </View>
      </View>

      <View style={[styles.macrosRow, { backgroundColor: colors.surfaceLight }]}>
        <Text style={[styles.macroItem, { color: colors.indigo }]}>
          P: <Text style={styles.macroVal}>{Math.round(item.protein_g)}g</Text>
        </Text>
        <Text style={[styles.macroItem, { color: colors.amber }]}>
          C: <Text style={styles.macroVal}>{Math.round(item.carbs_g)}g</Text>
        </Text>
        <Text style={[styles.macroItem, { color: colors.rose }]}>
          F: <Text style={styles.macroVal}>{Math.round(item.fat_g)}g</Text>
        </Text>
        {item.fiber_g > 0 && (
          <Text style={[styles.macroItem, { color: colors.emerald }]}>
            Fiber: <Text style={styles.macroVal}>{Math.round(item.fiber_g)}g</Text>
          </Text>
        )}
      </View>

      {isEditing && (
        <PortionEditor
          item={item}
          originalItem={originalItem}
          onChange={onUpdate}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 14,
    marginBottom: 12,
  },
  headerRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  titleInfo: {
    flexDirection: "row",
    alignItems: "center",
    flex: 1,
    marginRight: 8,
  },
  indexBadge: {
    width: 26,
    height: 26,
    borderRadius: 13,
    alignItems: "center",
    justifyContent: "center",
    marginRight: 10,
  },
  indexText: {
    fontSize: 13,
    fontWeight: "800",
  },
  nameContainer: {
    flex: 1,
  },
  foodName: {
    fontSize: 16,
    fontWeight: "700",
    marginBottom: 2,
  },
  metaRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  portionSubtitle: {
    fontSize: 13,
    fontWeight: "500",
  },
  confidencePill: {
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6,
  },
  confidenceText: {
    fontSize: 10,
    fontWeight: "700",
  },
  actions: {
    flexDirection: "row",
    gap: 6,
  },
  actionBtn: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: "center",
    justifyContent: "center",
  },
  macrosRow: {
    flexDirection: "row",
    gap: 14,
    paddingVertical: 6,
    paddingHorizontal: 10,
    borderRadius: 8,
    marginTop: 10,
  },
  macroItem: {
    fontSize: 12,
    fontWeight: "600",
  },
  macroVal: {
    fontWeight: "700",
  },
});
