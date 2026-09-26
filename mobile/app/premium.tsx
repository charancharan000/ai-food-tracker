import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useAuth } from "../hooks/useAuth";
import { useTheme } from "../hooks/useTheme";
import { storage } from "../utils/storage";

interface PremiumFeature {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  description: string;
  badge?: string;
  route?: string;
}

const PREMIUM_FEATURES: PremiumFeature[] = [
  {
    icon: "restaurant-outline",
    title: "AI Smart Meal Planner",
    description: "Generate customized 7-day meal plans and healthy chef recipes scaled to your exact calorie and macro targets.",
    badge: "VIP EXCLUSIVE",
    route: "/meal-planner",
  },
  {
    icon: "chatbubbles-outline",
    title: "AI Nutrition Coach",
    description: "Direct chat with an AI nutritionist for personalized meal substitutions, timing advice, and diet questions.",
    badge: "AI ASSISTANT",
    route: "/nutrition-coach",
  },
  {
    icon: "analytics-outline",
    title: "Advanced Micronutrient Tracking",
    description: "In-depth analytics for Vitamins A, C, D, B12, Iron, Calcium, Potassium, Magnesium, and Omega-3 fatty acids.",
    badge: "CLINICAL GRADE",
  },
  {
    icon: "camera-outline",
    title: "Unlimited Instant Food Scans",
    description: "Zero wait time, highest priority AI neural analysis for unlimited meal photos and multi-dish plates.",
  },
  {
    icon: "document-text-outline",
    title: "PDF Nutrition Export",
    description: "Export clean clinical reports of your meals, macros, and adherence to share with personal trainers or dietitians.",
  },
  {
    icon: "color-palette-outline",
    title: "Exclusive Pro Dark Themes",
    description: "Unlock Cyber Gold and Midnight Emerald premium visual themes with custom app badges.",
  },
];

export default function PremiumMembershipScreen() {
  const { user, setUserState } = useAuth();
  const { colors } = useTheme();
  const router = useRouter();

  const isPremium = user?.is_premium || false;
  const [selectedPlan, setSelectedPlan] = useState<"annual" | "monthly">("annual");

  const handleToggleMembership = async () => {
    if (!user) return;
    const newStatus = !isPremium;
    const updatedUser = {
      ...user,
      is_premium: newStatus,
      membership_tier: newStatus ? ("pro" as const) : ("free" as const),
    };
    setUserState(updatedUser);
    await storage.setUser(updatedUser);

    if (newStatus) {
      Alert.alert(
        "Welcome to Pro VIP!",
        "Your Pro Membership has been activated. Enjoy unlimited AI meal planning, nutrition coach chat, and priority scans."
      );
    } else {
      Alert.alert("Membership Cancelled", "Your account has been switched back to the Free plan.");
    }
  };

  const handleNavigateFeature = (route?: string) => {
    if (!route) return;
    if (!isPremium) {
      Alert.alert(
        "Pro Feature Locked",
        "Activate your VIP Membership below to unlock this feature.",
        [
          { text: "Cancel", style: "cancel" },
          { text: "Activate Free VIP", onPress: handleToggleMembership },
        ]
      );
      return;
    }
    router.push(route as any);
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      <View style={[styles.header, { borderBottomColor: colors.border }]}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()} activeOpacity={0.7}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <Text style={[styles.headerTitle, { color: colors.text }]}>Membership Club</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <View style={[styles.bannerCard, { backgroundColor: "#1A162B", borderColor: colors.primary }]}>
          <View style={styles.vipCrownCircle}>
            <Ionicons name="ribbon" size={32} color="#F59E0B" />
          </View>
          <Text style={styles.bannerTag}>NUTRISCAN AI PRO</Text>
          <Text style={styles.bannerHeading}>
            {isPremium ? "VIP Member Active" : "Supercharge Your Nutrition"}
          </Text>
          <Text style={styles.bannerSubtext}>
            {isPremium
              ? "You have full access to all extra premium features, meal planners, and the AI coach."
              : "Unlock clinical-grade nutrition intelligence, automated meal planning, and an on-demand AI coach."}
          </Text>

          <View style={styles.statusPill}>
            <View style={[styles.statusDot, { backgroundColor: isPremium ? "#10B981" : "#F59E0B" }]} />
            <Text style={styles.statusText}>
              {isPremium ? "PRO VIP TIER ACTIVATED" : "CURRENTLY ON FREE TIER"}
            </Text>
          </View>
        </View>

        <View style={[styles.section, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>Exclusive Extra Features</Text>
          <Text style={[styles.sectionSubtitle, { color: colors.textSecondary }]}>
            Available only to Pro membership holders
          </Text>

          <View style={styles.featuresList}>
            {PREMIUM_FEATURES.map((item, idx) => (
              <TouchableOpacity
                key={idx}
                style={[
                  styles.featureRow,
                  { backgroundColor: colors.surfaceHighlight, borderColor: colors.border },
                ]}
                onPress={() => item.route && handleNavigateFeature(item.route)}
                activeOpacity={item.route ? 0.7 : 1}
              >
                <View style={[styles.featureIconBox, { backgroundColor: `${colors.primary}25` }]}>
                  <Ionicons name={item.icon} size={22} color={colors.primary} />
                </View>

                <View style={styles.featureTextBox}>
                  <View style={styles.featureTitleRow}>
                    <Text style={[styles.featureTitle, { color: colors.text }]}>{item.title}</Text>
                    {item.badge && (
                      <View style={[styles.featureBadge, { backgroundColor: `${colors.amber}20` }]}>
                        <Text style={[styles.featureBadgeText, { color: colors.amber }]}>{item.badge}</Text>
                      </View>
                    )}
                  </View>
                  <Text style={[styles.featureDesc, { color: colors.textSecondary }]}>{item.description}</Text>
                </View>

                {item.route && (
                  <Ionicons name="chevron-forward" size={18} color={colors.textMuted} />
                )}
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {!isPremium && (
          <View style={[styles.planCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
            <Text style={[styles.planHeading, { color: colors.text }]}>Choose Your Membership</Text>

            <View style={styles.planOptions}>
              <TouchableOpacity
                style={[
                  styles.planOption,
                  {
                    backgroundColor: selectedPlan === "annual" ? `${colors.primary}15` : colors.surfaceHighlight,
                    borderColor: selectedPlan === "annual" ? colors.primary : colors.border,
                  },
                ]}
                onPress={() => setSelectedPlan("annual")}
                activeOpacity={0.8}
              >
                <View style={styles.planHeader}>
                  <Text style={[styles.planName, { color: colors.text }]}>Annual VIP</Text>
                  <View style={[styles.saveBadge, { backgroundColor: colors.primary }]}>
                    <Text style={styles.saveBadgeText}>SAVE 50%</Text>
                  </View>
                </View>
                <Text style={[styles.planPrice, { color: colors.primary }]}>$4.99 / mo</Text>
                <Text style={[styles.planBilled, { color: colors.textMuted }]}>Billed annually ($59.99/yr)</Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[
                  styles.planOption,
                  {
                    backgroundColor: selectedPlan === "monthly" ? `${colors.primary}15` : colors.surfaceHighlight,
                    borderColor: selectedPlan === "monthly" ? colors.primary : colors.border,
                  },
                ]}
                onPress={() => setSelectedPlan("monthly")}
                activeOpacity={0.8}
              >
                <Text style={[styles.planName, { color: colors.text }]}>Monthly Pass</Text>
                <Text style={[styles.planPrice, { color: colors.text }]}>$9.99 / mo</Text>
                <Text style={[styles.planBilled, { color: colors.textMuted }]}>Billed monthly, cancel anytime</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}

        <TouchableOpacity
          style={[
            styles.actionButton,
            { backgroundColor: isPremium ? colors.surfaceHighlight : colors.primary, borderColor: colors.border },
          ]}
          onPress={handleToggleMembership}
          activeOpacity={0.8}
        >
          <Ionicons
            name={isPremium ? "close-circle-outline" : "star"}
            size={18}
            color={isPremium ? colors.danger : "#FFFFFF"}
          />
          <Text
            style={[
              styles.actionButtonText,
              { color: isPremium ? colors.danger : "#FFFFFF" },
            ]}
          >
            {isPremium ? "Deactivate Pro Membership" : "Activate Pro VIP (Instant Access)"}
          </Text>
        </TouchableOpacity>

        <View style={styles.footerInfo}>
          <Text style={[styles.footerInfoText, { color: colors.textMuted }]}>
            Subscriptions can be managed anytime. Pro features are available on all your mobile devices.
          </Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  backBtn: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: "800",
  },
  scrollContent: {
    padding: 16,
    gap: 16,
    paddingBottom: 40,
  },
  bannerCard: {
    borderRadius: 22,
    borderWidth: 1.5,
    padding: 22,
    alignItems: "center",
  },
  vipCrownCircle: {
    width: 64,
    height: 64,
    borderRadius: 32,
    backgroundColor: "rgba(245, 158, 11, 0.15)",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 12,
  },
  bannerTag: {
    color: "#F59E0B",
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 1.5,
    marginBottom: 4,
  },
  bannerHeading: {
    color: "#FFFFFF",
    fontSize: 22,
    fontWeight: "800",
    marginBottom: 8,
    textAlign: "center",
  },
  bannerSubtext: {
    color: "#94A3B8",
    fontSize: 13,
    textAlign: "center",
    lineHeight: 19,
    marginBottom: 16,
  },
  statusPill: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(255, 255, 255, 0.08)",
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    gap: 8,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  statusText: {
    color: "#FFFFFF",
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.5,
  },
  section: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 18,
  },
  sectionTitle: {
    fontSize: 17,
    fontWeight: "800",
    marginBottom: 2,
  },
  sectionSubtitle: {
    fontSize: 13,
    marginBottom: 14,
  },
  featuresList: {
    gap: 12,
  },
  featureRow: {
    flexDirection: "row",
    alignItems: "center",
    padding: 14,
    borderRadius: 14,
    borderWidth: 1,
    gap: 12,
  },
  featureIconBox: {
    width: 44,
    height: 44,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
  },
  featureTextBox: {
    flex: 1,
  },
  featureTitleRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    marginBottom: 3,
    flexWrap: "wrap",
  },
  featureTitle: {
    fontSize: 14,
    fontWeight: "700",
  },
  featureBadge: {
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6,
  },
  featureBadgeText: {
    fontSize: 9,
    fontWeight: "800",
    letterSpacing: 0.5,
  },
  featureDesc: {
    fontSize: 12,
    lineHeight: 16,
  },
  planCard: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 18,
  },
  planHeading: {
    fontSize: 16,
    fontWeight: "800",
    marginBottom: 12,
  },
  planOptions: {
    gap: 10,
  },
  planOption: {
    borderRadius: 14,
    borderWidth: 1.5,
    padding: 14,
  },
  planHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 4,
  },
  planName: {
    fontSize: 15,
    fontWeight: "700",
  },
  saveBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 8,
  },
  saveBadgeText: {
    color: "#FFFFFF",
    fontSize: 10,
    fontWeight: "800",
  },
  planPrice: {
    fontSize: 18,
    fontWeight: "800",
    marginBottom: 2,
  },
  planBilled: {
    fontSize: 12,
  },
  actionButton: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    height: 52,
    borderRadius: 14,
    borderWidth: 1,
  },
  actionButtonText: {
    fontSize: 16,
    fontWeight: "700",
  },
  footerInfo: {
    alignItems: "center",
    paddingHorizontal: 12,
  },
  footerInfoText: {
    fontSize: 12,
    textAlign: "center",
    lineHeight: 17,
  },
});
