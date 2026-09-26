import React, { useState, useRef } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useAuth } from "../hooks/useAuth";
import { useTheme } from "../hooks/useTheme";

interface ChatMessage {
  id: string;
  sender: "user" | "coach";
  text: string;
  time: string;
}

const PROMPT_SUGGESTIONS = [
  "High protein post-workout meal",
  "How to curb evening sugar cravings",
  "Healthy low-carb dinner ideas",
  "Best foods for muscle recovery",
];

export default function NutritionCoachScreen() {
  const { user } = useAuth();
  const { colors } = useTheme();
  const router = useRouter();

  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      sender: "coach",
      text: `Hello ${user?.name ? user.name.split(" ")[0] : "Friend"}! 👋 I'm your dedicated AI Nutrition Coach.\n\nYour target is ${user?.daily_calorie_target || 2000} kcal/day with a goal to ${user?.goal || "maintain"}. Ask me anything about meal substitutions, pre/post workout nutrition, or reaching your daily macros!`,
      time: "Just now",
    },
  ]);

  const scrollViewRef = useRef<ScrollView>(null);

  const generateCoachResponse = (query: string): string => {
    const q = query.toLowerCase();
    const targetCals = user?.daily_calorie_target || 2000;
    const proteinTarget = user?.protein_target || 140;

    if (q.includes("post-workout") || q.includes("workout")) {
      return `For optimal muscle recovery post-workout, aim for a 3:1 or 2:1 ratio of carbs to protein within 45 minutes of training.\n\nGreat options:\n• Whey isolate smoothie with 1 frozen banana & almond milk (~280 kcal, 30g protein)\n• 150g grilled chicken breast with 1 cup jasmine rice (~420 kcal, 40g protein)\n• Greek yogurt (0%) with a drizzle of honey & blueberries (~220 kcal, 22g protein)`;
    }

    if (q.includes("craving") || q.includes("sugar") || q.includes("sweet")) {
      return `Evening sugar cravings often indicate low protein earlier in the day or slight dehydration.\n\nSmart swaps:\n1. Frozen grapes or mixed berries with a dash of cinnamon (~60 kcal)\n2. 2 squares of 85%+ Dark Chocolate with a glass of water (~110 kcal)\n3. Chamomile tea with 1 tsp raw honey to calm cortisol levels.`;
    }

    if (q.includes("low-carb") || q.includes("keto") || q.includes("dinner")) {
      return `Here is a nutrient-packed low-carb dinner fitting your ${targetCals} kcal plan:\n\nPan-seared Atlantic Salmon (180g) with garlic butter roasted asparagus & riced cauliflower.\n• Calories: 440 kcal\n• Protein: 42g\n• Net Carbs: 6g\n• Healthy Fats: 26g (rich in Omega-3 EPA/DHA)`;
    }

    if (q.includes("protein")) {
      return `Your daily protein target is ${proteinTarget}g. To hit this consistently without feeling stuffed:\n\n• Start breakfast with 30g protein (eggs + egg whites or Greek yogurt)\n• Ensure lunch and dinner have at least 40g (lean poultry, fish, tofu, or lean beef)\n• Use a high-quality whey or plant isolate shake if you're ever falling short towards the evening.`;
    }

    return `Based on your goal to ${user?.goal || "maintain health"}, consistency and whole food density are key. Focus on lean protein sources, complex fibrous carbs, and healthy monounsaturated fats. Feel free to ask about any specific food item or recipe substitution!`;
  };

  const handleSend = (textToSend?: string) => {
    const query = (textToSend || input).trim();
    if (!query) return;

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: "user",
      text: query,
      time: "Now",
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    setTimeout(() => {
      const responseText = generateCoachResponse(query);
      const coachMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "coach",
        text: responseText,
        time: "Now",
      };
      setMessages((prev) => [...prev, coachMsg]);
      scrollViewRef.current?.scrollToEnd({ animated: true });
    }, 450);
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      <View style={[styles.header, { borderBottomColor: colors.border }]}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()} activeOpacity={0.7}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <View style={styles.headerTitleWrap}>
          <Text style={[styles.headerTitle, { color: colors.text }]}>AI Nutrition Coach</Text>
          <Text style={[styles.headerStatus, { color: "#10B981" }]}>Online • Pro Intelligence</Text>
        </View>
        <View style={[styles.vipPill, { backgroundColor: `${colors.amber}20` }]}>
          <Ionicons name="sparkles" size={12} color={colors.amber} />
          <Text style={[styles.vipPillText, { color: colors.amber }]}>AI PRO</Text>
        </View>
      </View>

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === "ios" ? "padding" : undefined}
      >
        <ScrollView
          ref={scrollViewRef}
          contentContainerStyle={styles.chatScroll}
          showsVerticalScrollIndicator={false}
          onContentSizeChange={() => scrollViewRef.current?.scrollToEnd({ animated: true })}
        >
          {messages.map((m) => {
            const isUser = m.sender === "user";
            return (
              <View
                key={m.id}
                style={[
                  styles.messageBubbleWrap,
                  isUser ? styles.userBubbleWrap : styles.coachBubbleWrap,
                ]}
              >
                {!isUser && (
                  <View style={[styles.coachAvatar, { backgroundColor: `${colors.primary}20` }]}>
                    <Ionicons name="nutrition" size={18} color={colors.primary} />
                  </View>
                )}
                <View
                  style={[
                    styles.bubble,
                    isUser
                      ? [styles.userBubble, { backgroundColor: colors.primary }]
                      : [
                          styles.coachBubble,
                          { backgroundColor: colors.surface, borderColor: colors.border },
                        ],
                  ]}
                >
                  <Text
                    style={[
                      styles.bubbleText,
                      { color: isUser ? "#FFFFFF" : colors.text },
                    ]}
                  >
                    {m.text}
                  </Text>
                </View>
              </View>
            );
          })}
        </ScrollView>

        <View style={styles.suggestionsStrip}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.suggestionsScroll}>
            {PROMPT_SUGGESTIONS.map((item, idx) => (
              <TouchableOpacity
                key={idx}
                style={[
                  styles.suggestionChip,
                  { backgroundColor: colors.surfaceHighlight, borderColor: colors.border },
                ]}
                onPress={() => handleSend(item)}
                activeOpacity={0.7}
              >
                <Text style={[styles.suggestionText, { color: colors.textSecondary }]}>{item}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        <View style={[styles.inputBar, { backgroundColor: colors.surface, borderTopColor: colors.border }]}>
          <TextInput
            style={[
              styles.textInput,
              { backgroundColor: colors.surfaceHighlight, color: colors.text, borderColor: colors.border },
            ]}
            placeholder="Ask your coach anything about food..."
            placeholderTextColor={colors.textMuted}
            value={input}
            onChangeText={setInput}
            onSubmitEditing={() => handleSend()}
            returnKeyType="send"
          />
          <TouchableOpacity
            style={[styles.sendButton, { backgroundColor: colors.primary }]}
            onPress={() => handleSend()}
            disabled={!input.trim()}
            activeOpacity={0.8}
          >
            <Ionicons name="send" size={18} color="#FFFFFF" />
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
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
  headerTitleWrap: {
    alignItems: "center",
  },
  headerTitle: {
    fontSize: 16,
    fontWeight: "800",
  },
  headerStatus: {
    fontSize: 11,
    fontWeight: "600",
  },
  vipPill: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  vipPillText: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 0.5,
  },
  chatScroll: {
    padding: 16,
    gap: 12,
    paddingBottom: 16,
  },
  messageBubbleWrap: {
    flexDirection: "row",
    gap: 8,
    maxWidth: "86%",
  },
  userBubbleWrap: {
    alignSelf: "flex-end",
    flexDirection: "row-reverse",
  },
  coachBubbleWrap: {
    alignSelf: "flex-start",
  },
  coachAvatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: "center",
    justifyContent: "center",
    marginTop: 4,
  },
  bubble: {
    borderRadius: 18,
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
  userBubble: {
    borderBottomRightRadius: 4,
  },
  coachBubble: {
    borderBottomLeftRadius: 4,
    borderWidth: 1,
  },
  bubbleText: {
    fontSize: 14,
    lineHeight: 20,
  },
  suggestionsStrip: {
    paddingVertical: 6,
  },
  suggestionsScroll: {
    paddingHorizontal: 12,
    gap: 8,
  },
  suggestionChip: {
    paddingHorizontal: 12,
    paddingVertical: 7,
    borderRadius: 16,
    borderWidth: 1,
  },
  suggestionText: {
    fontSize: 12,
    fontWeight: "600",
  },
  inputBar: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderTopWidth: 1,
    gap: 8,
  },
  textInput: {
    flex: 1,
    height: 44,
    borderRadius: 22,
    borderWidth: 1,
    paddingHorizontal: 16,
    fontSize: 14,
  },
  sendButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: "center",
    justifyContent: "center",
  },
});
