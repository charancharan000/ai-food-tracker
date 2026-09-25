import React, { createContext, useContext, useState, useEffect } from "react";
import { storage } from "../utils/storage";

export type ThemePaletteId = "cyber_violet" | "sunset_coral" | "midnight_emerald" | "ocean_cobalt";

export interface ColorTheme {
  background: string;
  surface: string;
  surfaceLight: string;
  surfaceHighlight: string;
  border: string;
  borderSubtle: string;
  text: string;
  textSecondary: string;
  textMuted: string;
  primary: string;
  primaryLight: string;
  primaryGlow: string;
  emerald: string;
  indigo: string;
  amber: string;
  rose: string;
  cyan: string;
  danger: string;
}

export interface ThemePreset {
  id: ThemePaletteId;
  name: string;
  description: string;
  accent: string;
  gradientColors: [string, string];
}

export const THEME_PRESETS: ThemePreset[] = [
  {
    id: "cyber_violet",
    name: "Cyber Violet",
    description: "Deep obsidian velvet with vivid electric violet",
    accent: "#8B5CF6",
    gradientColors: ["#8B5CF6", "#6366F1"],
  },
  {
    id: "sunset_coral",
    name: "Sunset Coral",
    description: "Warm carbon with glowing sunset coral & amber",
    accent: "#FF5376",
    gradientColors: ["#FF5376", "#FBA94B"],
  },
  {
    id: "ocean_cobalt",
    name: "Ocean Cobalt",
    description: "Deep midnight abyss with electric sapphire & azure",
    accent: "#3B82F6",
    gradientColors: ["#3B82F6", "#00D2FF"],
  },
  {
    id: "midnight_emerald",
    name: "Neon Emerald",
    description: "Deep obsidian slate with luminous mint & jade",
    accent: "#10B981",
    gradientColors: ["#10B981", "#05E28B"],
  },
];

const darkPalettes: Record<ThemePaletteId, ColorTheme> = {
  cyber_violet: {
    background: "#090A11",
    surface: "#121422",
    surfaceLight: "#1A1D2E",
    surfaceHighlight: "#24283F",
    border: "#20253B",
    borderSubtle: "rgba(255, 255, 255, 0.07)",
    text: "#F8FAFC",
    textSecondary: "#94A3B8",
    textMuted: "#64748B",
    primary: "#8B5CF6",
    primaryLight: "#A78BFA",
    primaryGlow: "rgba(139, 92, 246, 0.35)",
    emerald: "#10B981",
    indigo: "#8B5CF6",
    amber: "#F59E0B",
    rose: "#FF3366",
    cyan: "#00D2FF",
    danger: "#EF4444",
  },
  sunset_coral: {
    background: "#0C0D14",
    surface: "#161724",
    surfaceLight: "#202232",
    surfaceHighlight: "#2B2D43",
    border: "#26293F",
    borderSubtle: "rgba(255, 255, 255, 0.07)",
    text: "#FDFEFE",
    textSecondary: "#A1A8BA",
    textMuted: "#697084",
    primary: "#FF5376",
    primaryLight: "#FF7597",
    primaryGlow: "rgba(255, 83, 118, 0.35)",
    emerald: "#10B981",
    indigo: "#FF5376",
    amber: "#FBA94B",
    rose: "#FF3366",
    cyan: "#38BDF8",
    danger: "#EF4444",
  },
  ocean_cobalt: {
    background: "#070D1B",
    surface: "#0E1831",
    surfaceLight: "#162345",
    surfaceHighlight: "#1F315E",
    border: "#1D305A",
    borderSubtle: "rgba(255, 255, 255, 0.07)",
    text: "#F8FAFC",
    textSecondary: "#94A3B8",
    textMuted: "#64748B",
    primary: "#3B82F6",
    primaryLight: "#60A5FA",
    primaryGlow: "rgba(59, 130, 246, 0.35)",
    emerald: "#10B981",
    indigo: "#60A5FA",
    amber: "#FBBF24",
    rose: "#F43F5E",
    cyan: "#00D2FF",
    danger: "#EF4444",
  },
  midnight_emerald: {
    background: "#070E14",
    surface: "#0E1C27",
    surfaceLight: "#162937",
    surfaceHighlight: "#203749",
    border: "#1E3446",
    borderSubtle: "rgba(255, 255, 255, 0.07)",
    text: "#F8FAFC",
    textSecondary: "#94A3B8",
    textMuted: "#64748B",
    primary: "#10B981",
    primaryLight: "#34D399",
    primaryGlow: "rgba(16, 185, 129, 0.35)",
    emerald: "#10B981",
    indigo: "#6366F1",
    amber: "#F59E0B",
    rose: "#F43F5E",
    cyan: "#06B6D4",
    danger: "#EF4444",
  },
};

const lightPalettes: Record<ThemePaletteId, ColorTheme> = {
  cyber_violet: {
    background: "#F6F7FB",
    surface: "#FFFFFF",
    surfaceLight: "#F1F3F9",
    surfaceHighlight: "#EDE9FE",
    border: "#E2E8F0",
    borderSubtle: "rgba(0, 0, 0, 0.04)",
    text: "#0F172A",
    textSecondary: "#475569",
    textMuted: "#94A3B8",
    primary: "#7C3AED",
    primaryLight: "#8B5CF6",
    primaryGlow: "rgba(124, 58, 237, 0.2)",
    emerald: "#059669",
    indigo: "#7C3AED",
    amber: "#D97706",
    rose: "#E11D48",
    cyan: "#0891B2",
    danger: "#DC2626",
  },
  sunset_coral: {
    background: "#FAF7F6",
    surface: "#FFFFFF",
    surfaceLight: "#F8F2F1",
    surfaceHighlight: "#FFE8EC",
    border: "#E8E2E1",
    borderSubtle: "rgba(0, 0, 0, 0.04)",
    text: "#1A1516",
    textSecondary: "#524A4C",
    textMuted: "#998F91",
    primary: "#E11D48",
    primaryLight: "#FF5376",
    primaryGlow: "rgba(225, 29, 72, 0.2)",
    emerald: "#059669",
    indigo: "#E11D48",
    amber: "#D97706",
    rose: "#BE123C",
    cyan: "#0284C7",
    danger: "#DC2626",
  },
  ocean_cobalt: {
    background: "#F5F8FC",
    surface: "#FFFFFF",
    surfaceLight: "#EDF2F9",
    surfaceHighlight: "#DBEAFE",
    border: "#E2E8F0",
    borderSubtle: "rgba(0, 0, 0, 0.04)",
    text: "#0F172A",
    textSecondary: "#475569",
    textMuted: "#94A3B8",
    primary: "#2563EB",
    primaryLight: "#3B82F6",
    primaryGlow: "rgba(37, 99, 235, 0.2)",
    emerald: "#059669",
    indigo: "#2563EB",
    amber: "#D97706",
    rose: "#E11D48",
    cyan: "#0284C7",
    danger: "#DC2626",
  },
  midnight_emerald: {
    background: "#F5FAF8",
    surface: "#FFFFFF",
    surfaceLight: "#EDF6F2",
    surfaceHighlight: "#D1FAE5",
    border: "#E2E8F0",
    borderSubtle: "rgba(0, 0, 0, 0.04)",
    text: "#0F172A",
    textSecondary: "#475569",
    textMuted: "#94A3B8",
    primary: "#059669",
    primaryLight: "#10B981",
    primaryGlow: "rgba(5, 150, 105, 0.2)",
    emerald: "#059669",
    indigo: "#4F46E5",
    amber: "#D97706",
    rose: "#E11D48",
    cyan: "#0891B2",
    danger: "#DC2626",
  },
};

interface ThemeContextType {
  theme: "dark" | "light";
  isDark: boolean;
  colors: ColorTheme;
  palette: ThemePaletteId;
  presets: ThemePreset[];
  toggleTheme: () => void;
  setThemeMode: (mode: "dark" | "light") => void;
  setPalette: (paletteId: ThemePaletteId) => void;
}

const ThemeContext = createContext<ThemeContextType>({
  theme: "dark",
  isDark: true,
  colors: darkPalettes.cyber_violet,
  palette: "cyber_violet",
  presets: THEME_PRESETS,
  toggleTheme: () => {},
  setThemeMode: () => {},
  setPalette: () => {},
});

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [palette, setPaletteState] = useState<ThemePaletteId>("cyber_violet");

  useEffect(() => {
    storage.getTheme().then((savedTheme) => {
      if (savedTheme === "light" || savedTheme === "dark") {
        setTheme(savedTheme);
      }
    });
    storage.getThemePalette().then((savedPalette) => {
      if (savedPalette && darkPalettes[savedPalette as ThemePaletteId]) {
        setPaletteState(savedPalette as ThemePaletteId);
      }
    });
  }, []);

  const toggleTheme = () => {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    storage.setTheme(next);
  };

  const setThemeMode = (mode: "dark" | "light") => {
    setTheme(mode);
    storage.setTheme(mode);
  };

  const setPalette = (paletteId: ThemePaletteId) => {
    setPaletteState(paletteId);
    storage.setThemePalette(paletteId);
  };

  const isDark = theme === "dark";
  const paletteTable = isDark ? darkPalettes : lightPalettes;
  const colors = paletteTable[palette] || paletteTable.cyber_violet;

  return (
    <ThemeContext.Provider
      value={{
        theme,
        isDark,
        colors,
        palette,
        presets: THEME_PRESETS,
        toggleTheme,
        setThemeMode,
        setPalette,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
