import React, { useState, useEffect, useCallback } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Linking,
  Alert,
  RefreshControl,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../hooks/useTheme";
import { sheetsService, RegistrationRecord, LIVE_SHEET_VIEW_URL } from "../services/sheetsService";

export default function AdminRegistrationsScreen() {
  const { colors } = useTheme();
  const router = useRouter();

  const [records, setRecords] = useState<RegistrationRecord[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [isSyncing, setIsSyncing] = useState(false);

  const loadRecords = useCallback(async () => {
    try {
      const data = await sheetsService.getAdminRecords();
      setRecords(data);
    } finally {
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadRecords();
  }, [loadRecords]);

  const handleOpenLiveSheet = () => {
    Linking.openURL(LIVE_SHEET_VIEW_URL).catch(() => {
      Alert.alert("Link", `Live Sheet URL:\n${LIVE_SHEET_VIEW_URL}`);
    });
  };

  const handleSyncNow = async () => {
    try {
      setIsSyncing(true);
      const synced = await sheetsService.syncPendingRegistrations();
      await loadRecords();
      Alert.alert("Sync Complete", `${synced} pending registration(s) pushed to the live sheet.`);
    } catch {
      Alert.alert("Sync Error", "Could not complete sync.");
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      <View style={[styles.header, { borderBottomColor: colors.border }]}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()} activeOpacity={0.7}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <Text style={[styles.headerTitle, { color: colors.text }]}>Live Registrations Space</Text>
        <TouchableOpacity onPress={handleOpenLiveSheet} activeOpacity={0.7}>
          <Ionicons name="open-outline" size={22} color={colors.primary} />
        </TouchableOpacity>
      </View>

      <ScrollView
        contentContainerStyle={styles.scrollContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={loadRecords} />}
        showsVerticalScrollIndicator={false}
      >
        <View style={[styles.bannerCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <View style={styles.bannerHeader}>
            <View style={[styles.sheetIconBox, { backgroundColor: "#10B98120" }]}>
              <Ionicons name="grid-outline" size={24} color="#10B981" />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={[styles.bannerHeading, { color: colors.text }]}>Private Registration Space</Text>
              <Text style={[styles.bannerDesc, { color: colors.textSecondary }]}>
                All new user registrations stream live to your private space.
              </Text>
            </View>
          </View>

          <View style={styles.actionButtonsRow}>
            <TouchableOpacity
              style={[styles.openLiveBtn, { backgroundColor: "#10B981" }]}
              onPress={handleOpenLiveSheet}
              activeOpacity={0.8}
            >
              <Ionicons name="globe-outline" size={16} color="#FFFFFF" />
              <Text style={styles.openLiveBtnText}>Open Live Web Sheet</Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[styles.syncBtn, { borderColor: colors.border, backgroundColor: colors.surfaceHighlight }]}
              onPress={handleSyncNow}
              disabled={isSyncing}
              activeOpacity={0.7}
            >
              <Ionicons name="sync-outline" size={16} color={colors.text} />
              <Text style={[styles.syncBtnText, { color: colors.text }]}>
                {isSyncing ? "Syncing..." : "Sync All"}
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        <View style={[styles.tableCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <View style={styles.tableCardHeader}>
            <Text style={[styles.tableTitle, { color: colors.text }]}>
              User Registrations ({records.length})
            </Text>
            <Text style={[styles.tableSubtitle, { color: colors.textMuted }]}>Pull to refresh</Text>
          </View>

          {records.length === 0 ? (
            <View style={styles.emptyState}>
              <Ionicons name="file-tray-outline" size={36} color={colors.textMuted} />
              <Text style={[styles.emptyText, { color: colors.textSecondary }]}>
                No registrations logged on this device yet.
              </Text>
              <Text style={[styles.emptySubtext, { color: colors.textMuted }]}>
                Registrations made on any device stream live to the Web Sheet.
              </Text>
            </View>
          ) : (
            <View style={styles.recordsList}>
              {records.map((r, i) => (
                <View
                  key={r.id || i}
                  style={[
                    styles.recordCard,
                    { backgroundColor: colors.surfaceHighlight, borderColor: colors.border },
                  ]}
                >
                  <View style={styles.recordTopRow}>
                    <View style={styles.recordUserGroup}>
                      <Text style={[styles.recordName, { color: colors.text }]}>{r.name}</Text>
                      <Text style={[styles.recordEmail, { color: colors.textSecondary }]}>{r.email}</Text>
                    </View>
                    <View style={styles.badgeGroup}>
                      <View
                        style={[
                          styles.tierBadge,
                          { backgroundColor: r.membership_tier === "pro" ? `${colors.amber}25` : `${colors.primary}20` },
                        ]}
                      >
                        <Text
                          style={[
                            styles.tierBadgeText,
                            { color: r.membership_tier === "pro" ? colors.amber : colors.primary },
                          ]}
                        >
                          {(r.membership_tier || "free").toUpperCase()}
                        </Text>
                      </View>
                      <View style={[styles.syncStatusDot, { backgroundColor: r.synced ? "#10B981" : colors.amber }]} />
                    </View>
                  </View>

                  <View style={[styles.detailsGrid, { borderTopColor: colors.border }]}>
                    <View style={styles.detailCol}>
                      <Text style={[styles.detailVal, { color: colors.text }]}>{r.age || "--"} y/o</Text>
                      <Text style={[styles.detailLbl, { color: colors.textMuted }]}>Age</Text>
                    </View>
                    <View style={styles.detailCol}>
                      <Text style={[styles.detailVal, { color: colors.text }]}>{r.gender || "--"}</Text>
                      <Text style={[styles.detailLbl, { color: colors.textMuted }]}>Gender</Text>
                    </View>
                    <View style={styles.detailCol}>
                      <Text style={[styles.detailVal, { color: colors.text }]}>{r.weight_kg || "--"} kg</Text>
                      <Text style={[styles.detailLbl, { color: colors.textMuted }]}>Weight</Text>
                    </View>
                    <View style={styles.detailCol}>
                      <Text style={[styles.detailVal, { color: colors.primary }]}>
                        {r.daily_calorie_target || "--"}
                      </Text>
                      <Text style={[styles.detailLbl, { color: colors.textMuted }]}>Cal Target</Text>
                    </View>
                  </View>

                  <View style={styles.recordFooter}>
                    <Text style={[styles.recordTime, { color: colors.textMuted }]}>
                      {r.registered_at ? new Date(r.registered_at).toLocaleString() : ""}
                    </Text>
                    <Text style={[styles.syncStatusText, { color: r.synced ? "#10B981" : colors.amber }]}>
                      {r.synced ? "✓ Live Synced" : "Pending Webhook"}
                    </Text>
                  </View>
                </View>
              ))}
            </View>
          )}
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
    borderRadius: 20,
    borderWidth: 1,
    padding: 18,
  },
  bannerHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    marginBottom: 16,
  },
  sheetIconBox: {
    width: 48,
    height: 48,
    borderRadius: 14,
    alignItems: "center",
    justifyContent: "center",
  },
  bannerHeading: {
    fontSize: 16,
    fontWeight: "800",
    marginBottom: 2,
  },
  bannerDesc: {
    fontSize: 12,
    lineHeight: 16,
  },
  actionButtonsRow: {
    flexDirection: "row",
    gap: 10,
  },
  openLiveBtn: {
    flex: 1.3,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    height: 44,
    borderRadius: 12,
  },
  openLiveBtnText: {
    color: "#FFFFFF",
    fontSize: 13,
    fontWeight: "700",
  },
  syncBtn: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
    height: 44,
    borderRadius: 12,
    borderWidth: 1,
  },
  syncBtnText: {
    fontSize: 13,
    fontWeight: "700",
  },
  tableCard: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 18,
  },
  tableCardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 14,
  },
  tableTitle: {
    fontSize: 16,
    fontWeight: "800",
  },
  tableSubtitle: {
    fontSize: 12,
  },
  emptyState: {
    alignItems: "center",
    paddingVertical: 32,
    gap: 6,
  },
  emptyText: {
    fontSize: 14,
    fontWeight: "600",
  },
  emptySubtext: {
    fontSize: 12,
    textAlign: "center",
  },
  recordsList: {
    gap: 12,
  },
  recordCard: {
    borderRadius: 14,
    borderWidth: 1,
    padding: 14,
  },
  recordTopRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 10,
  },
  recordUserGroup: {
    flex: 1,
  },
  recordName: {
    fontSize: 15,
    fontWeight: "800",
    marginBottom: 2,
  },
  recordEmail: {
    fontSize: 12,
  },
  badgeGroup: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },
  tierBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  tierBadgeText: {
    fontSize: 10,
    fontWeight: "800",
  },
  syncStatusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  detailsGrid: {
    flexDirection: "row",
    borderTopWidth: 1,
    paddingTop: 10,
    marginBottom: 8,
  },
  detailCol: {
    flex: 1,
    alignItems: "center",
  },
  detailVal: {
    fontSize: 13,
    fontWeight: "700",
  },
  detailLbl: {
    fontSize: 10,
    marginTop: 2,
  },
  recordFooter: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  recordTime: {
    fontSize: 11,
  },
  syncStatusText: {
    fontSize: 11,
    fontWeight: "700",
  },
});
