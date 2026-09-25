export function formatCalories(val: number): string {
  return Math.round(val).toLocaleString();
}

export function formatGrams(val: number): string {
  return `${Math.round(val)} g`;
}

export function formatMg(val: number): string {
  return `${Math.round(val)} mg`;
}

export function formatDateLabel(dateString: string): string {
  const d = new Date(dateString);
  const now = new Date();
  
  const isToday = d.toDateString() === now.toDateString();
  if (isToday) return "Today";
  
  const yesterday = new Date();
  yesterday.setDate(now.getDate() - 1);
  if (d.toDateString() === yesterday.toDateString()) return "Yesterday";
  
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

export function formatTime(dateTimeStr: string): string {
  try {
    const d = new Date(dateTimeStr);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  } catch {
    return "";
  }
}

export const MACRO_COLORS = {
  calories: "#10B981",
  protein: "#6366F1",
  carbs: "#F59E0B",
  fat: "#EC4899",
  water: "#06B6D4",
  backgroundDark: "#0B0F19",
  cardDark: "#151C2C",
  borderDark: "#232F48",
  textPrimaryDark: "#F8FAFC",
  textSecondaryDark: "#94A3B8",
};
