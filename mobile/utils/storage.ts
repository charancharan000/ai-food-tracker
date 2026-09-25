import AsyncStorage from "@react-native-async-storage/async-storage";
import { User } from "../types/auth";

const TOKEN_KEY = "@nutriscan_token";
const USER_KEY = "@nutriscan_user";
const API_URL_KEY = "@nutriscan_api_url";
const THEME_KEY = "@nutriscan_theme";
const THEME_PALETTE_KEY = "@nutriscan_theme_palette";

export const DEFAULT_API_URL = "http://localhost:8000/api/v1";

export const storage = {
  async getToken(): Promise<string | null> {
    try {
      return await AsyncStorage.getItem(TOKEN_KEY);
    } catch {
      return null;
    }
  },

  async setToken(token: string): Promise<void> {
    try {
      await AsyncStorage.setItem(TOKEN_KEY, token);
    } catch (e) {
      console.error("Failed to save auth token", e);
    }
  },

  async removeToken(): Promise<void> {
    try {
      await AsyncStorage.removeItem(TOKEN_KEY);
    } catch (e) {
      console.error("Failed to remove auth token", e);
    }
  },

  async getUser(): Promise<User | null> {
    try {
      const data = await AsyncStorage.getItem(USER_KEY);
      return data ? JSON.parse(data) : null;
    } catch {
      return null;
    }
  },

  async setUser(user: User): Promise<void> {
    try {
      await AsyncStorage.setItem(USER_KEY, JSON.stringify(user));
    } catch (e) {
      console.error("Failed to save user", e);
    }
  },

  async removeUser(): Promise<void> {
    try {
      await AsyncStorage.removeItem(USER_KEY);
    } catch (e) {
      console.error("Failed to remove user", e);
    }
  },

  async getApiUrl(): Promise<string> {
    try {
      const url = await AsyncStorage.getItem(API_URL_KEY);
      return url || DEFAULT_API_URL;
    } catch {
      return DEFAULT_API_URL;
    }
  },

  async setApiUrl(url: string): Promise<void> {
    try {
      await AsyncStorage.setItem(API_URL_KEY, url);
    } catch (e) {
      console.error("Failed to save API URL", e);
    }
  },

  async getTheme(): Promise<"light" | "dark" | "system"> {
    try {
      const theme = await AsyncStorage.getItem(THEME_KEY);
      return (theme as "light" | "dark" | "system") || "dark";
    } catch {
      return "dark";
    }
  },

  async setTheme(theme: "light" | "dark" | "system"): Promise<void> {
    try {
      await AsyncStorage.setItem(THEME_KEY, theme);
    } catch (e) {
      console.error("Failed to save theme", e);
    }
  },

  async getThemePalette(): Promise<string> {
    try {
      const palette = await AsyncStorage.getItem(THEME_PALETTE_KEY);
      return palette || "cyber_violet";
    } catch {
      return "cyber_violet";
    }
  },

  async setThemePalette(palette: string): Promise<void> {
    try {
      await AsyncStorage.setItem(THEME_PALETTE_KEY, palette);
    } catch (e) {
      console.error("Failed to save theme palette", e);
    }
  },

  async clearAll(): Promise<void> {
    try {
      await AsyncStorage.removeItem(TOKEN_KEY);
      await AsyncStorage.removeItem(USER_KEY);
    } catch (e) {
      console.error("Failed to clear auth storage", e);
    }
  }
};
