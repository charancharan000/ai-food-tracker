import axios, { AxiosInstance } from "axios";
import { Platform } from "react-native";
import Constants from "expo-constants";
import { storage, DEFAULT_API_URL } from "../utils/storage";

export function getAutoDetectedBaseUrl(): string {
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
    return "http://10.0.2.2:8000/api/v1";
  }
  return "http://localhost:8000/api/v1";
}

export const apiClient: AxiosInstance = axios.create({
  baseURL: getAutoDetectedBaseUrl(),
  timeout: 35000,
  headers: {
    "Accept": "application/json",
  }
});

apiClient.interceptors.request.use(
  async (config) => {
    try {
      const customUrl = await storage.getApiUrl();
      if (customUrl && customUrl !== DEFAULT_API_URL) {
        config.baseURL = customUrl;
      }
      
      const token = await storage.getToken();
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch {
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 401) {
      await storage.removeToken();
      await storage.removeUser();
    }
    return Promise.reject(error);
  }
);
