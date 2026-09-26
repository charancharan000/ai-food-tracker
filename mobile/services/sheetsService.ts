import AsyncStorage from "@react-native-async-storage/async-storage";
import { User, RegisterPayload } from "../types/auth";
import { storage } from "../utils/storage";

const SHEETS_WEBHOOK_URL_KEY = "@nutriscan_sheets_webhook_url";
const PENDING_REGISTRATIONS_KEY = "@nutriscan_pending_registrations";
const ADMIN_REGISTRATIONS_KEY = "@nutriscan_admin_registrations_log";

export interface RegistrationRecord {
  id: string;
  name: string;
  email: string;
  age: number | string;
  gender: string;
  height_cm: number | string;
  weight_kg: number | string;
  activity_level: string;
  goal: string;
  daily_calorie_target: number | string;
  membership_tier: string;
  registered_at: string;
  device_platform?: string;
  synced: boolean;
}

export const sheetsService = {
  async getWebhookUrl(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem(SHEETS_WEBHOOK_URL_KEY);
    } catch {
      return null;
    }
  },

  async setWebhookUrl(url: string): Promise<void> {
    try {
      await AsyncStorage.setItem(SHEETS_WEBHOOK_URL_KEY, url.trim());
    } catch (e) {
      console.error("Failed to save Google Sheets webhook URL", e);
    }
  },

  async recordRegistration(user: User, payload?: RegisterPayload): Promise<void> {
    const record: RegistrationRecord = {
      id: "reg_" + Date.now(),
      name: user.name || payload?.name || "Unknown",
      email: user.email || payload?.email || "",
      age: user.age || payload?.age || "-",
      gender: user.gender || payload?.gender || "-",
      height_cm: user.height_cm || payload?.height_cm || "-",
      weight_kg: user.weight_kg || payload?.weight_kg || "-",
      activity_level: user.activity_level || payload?.activity_level || "-",
      goal: user.goal || payload?.goal || "-",
      daily_calorie_target: user.daily_calorie_target || payload?.daily_calorie_target || 2000,
      membership_tier: user.membership_tier || "free",
      registered_at: new Date().toISOString(),
      synced: false,
    };

    await this.saveLocalAdminRecord(record);
    await this.dispatchToGoogleSheets(record);
  },

  async saveLocalAdminRecord(record: RegistrationRecord): Promise<void> {
    try {
      const existing = await AsyncStorage.getItem(ADMIN_REGISTRATIONS_KEY);
      const list: RegistrationRecord[] = existing ? JSON.parse(existing) : [];
      list.unshift(record);
      await AsyncStorage.setItem(ADMIN_REGISTRATIONS_KEY, JSON.stringify(list));
    } catch (e) {
      console.error("Failed to save admin registration record", e);
    }
  },

  async getAdminRecords(): Promise<RegistrationRecord[]> {
    try {
      const existing = await AsyncStorage.getItem(ADMIN_REGISTRATIONS_KEY);
      return existing ? JSON.parse(existing) : [];
    } catch {
      return [];
    }
  },

  async dispatchToGoogleSheets(record: RegistrationRecord): Promise<boolean> {
    const webhookUrl = await this.getWebhookUrl();
    if (!webhookUrl) {
      await this.queuePendingRegistration(record);
      return false;
    }

    try {
      const response = await fetch(webhookUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(record),
      });

      if (response.ok) {
        await this.markRecordSynced(record.id);
        return true;
      } else {
        await this.queuePendingRegistration(record);
        return false;
      }
    } catch {
      await this.queuePendingRegistration(record);
      return false;
    }
  },

  async queuePendingRegistration(record: RegistrationRecord): Promise<void> {
    try {
      const pendingRaw = await AsyncStorage.getItem(PENDING_REGISTRATIONS_KEY);
      const pending: RegistrationRecord[] = pendingRaw ? JSON.parse(pendingRaw) : [];
      if (!pending.some((r) => r.id === record.id)) {
        pending.push(record);
        await AsyncStorage.setItem(PENDING_REGISTRATIONS_KEY, JSON.stringify(pending));
      }
    } catch (e) {
      console.error("Failed to queue pending registration", e);
    }
  },

  async markRecordSynced(recordId: string): Promise<void> {
    try {
      const existing = await AsyncStorage.getItem(ADMIN_REGISTRATIONS_KEY);
      if (existing) {
        const list: RegistrationRecord[] = JSON.parse(existing);
        const item = list.find((r) => r.id === recordId);
        if (item) item.synced = true;
        await AsyncStorage.setItem(ADMIN_REGISTRATIONS_KEY, JSON.stringify(list));
      }

      const pendingRaw = await AsyncStorage.getItem(PENDING_REGISTRATIONS_KEY);
      if (pendingRaw) {
        const pending: RegistrationRecord[] = JSON.parse(pendingRaw);
        const filtered = pending.filter((r) => r.id !== recordId);
        await AsyncStorage.setItem(PENDING_REGISTRATIONS_KEY, JSON.stringify(filtered));
      }
    } catch (e) {
      console.error("Failed to mark record synced", e);
    }
  },

  async syncPendingRegistrations(): Promise<number> {
    const webhookUrl = await this.getWebhookUrl();
    if (!webhookUrl) return 0;

    try {
      const pendingRaw = await AsyncStorage.getItem(PENDING_REGISTRATIONS_KEY);
      if (!pendingRaw) return 0;

      const pending: RegistrationRecord[] = JSON.parse(pendingRaw);
      let successCount = 0;

      for (const record of pending) {
        try {
          const resp = await fetch(webhookUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(record),
          });
          if (resp.ok) {
            await this.markRecordSynced(record.id);
            successCount++;
          }
        } catch {
        }
      }

      return successCount;
    } catch {
      return 0;
    }
  }
};
