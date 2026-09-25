import React from "react";
import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { ThemeProvider, useTheme } from "../hooks/useTheme";
import { AuthProvider } from "../hooks/useAuth";

function RootStack() {
  const { isDark } = useTheme();

  return (
    <>
      <StatusBar style={isDark ? "light" : "dark"} />
      <Stack screenOptions={{ headerShown: false, animation: "slide_from_right" }}>
        <Stack.Screen name="index" />
        <Stack.Screen name="(auth)/login" />
        <Stack.Screen name="(auth)/register" />
        <Stack.Screen name="(auth)/onboarding" />
        <Stack.Screen name="(auth)/profile-setup" />
        <Stack.Screen name="(tabs)" />
        <Stack.Screen
          name="meal/[id]"
          options={{
            headerShown: true,
            title: "Meal Details",
            headerBackTitle: "Back",
          }}
        />
        <Stack.Screen
          name="water"
          options={{
            headerShown: true,
            title: "Water Tracker",
            headerBackTitle: "Back",
          }}
        />
      </Stack>
    </>
  );
}

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <AuthProvider>
          <RootStack />
        </AuthProvider>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
