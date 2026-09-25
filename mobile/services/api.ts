import axios, { AxiosInstance } from "axios";
import { Platform } from "react-native";
import Constants from "expo-constants";
import { storage, DEFAULT_API_URL } from "../utils/storage";

// Determine sensible default host based on runtime platform and Expo host
export function getAutoDetectedBaseUrl(): string {
  // If running inside Expo Go on a physical phone, get the host IP from expoConfig
  const hostUri =
    Constants.expoConfig?.hostUri ||
    (Constants as any).manifest?.debuggerHost ||
    (Constants as any).manifest2?.extra?.expoClient?.hostUri;

  if (hostUri) {
    const ip = hostUri.split(":")[0];
    if (ip && ip !== "localhost" && ip !== "127.0.0.1") {
      return `http://${ip}:8000/api/v1`;
    }
  }

  if (Platform.OS === "android") {
    // 10.0.2.2 points to host machine from Android Emulator
    return "http://10.0.2.2:8000/api/v1";
  }
  return "http://localhost:8000/api/v1";
}

export const apiClient: AxiosInstance = axios.create({
  baseURL: getAutoDetectedBaseUrl(),
  timeout: 35000, // 35s for AI analysis
  headers: {
    "Accept": "application/json",
  }
});

// Request interceptor to add auth token and current configured API URL
apiClient.interceptors.request.use(
  async (config) => {
    try {
      // Dynamic base URL check from user settings
      const customUrl = await storage.getApiUrl();
      if (customUrl && customUrl !== DEFAULT_API_URL) {
        config.baseURL = customUrl;
      }
      
      const token = await storage.getToken();
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (e) {
      console.warn("Error attaching auth token to request", e);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 401) {
      // Token expired or invalid
      await storage.removeToken();
      await storage.removeUser();
    }
    return Promise.reject(error);
  }
);
