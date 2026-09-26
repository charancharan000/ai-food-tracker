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
  ActivityIndicator,
  Image,
  Alert,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import * as ImagePicker from "expo-image-picker";
import { useAuth } from "../hooks/useAuth";
import { useTheme } from "../hooks/useTheme";
import { coachService, CoachChatMessage } from "../services/coachService";
import { TypingDots } from "../components/TypingDots";
import { AnimatedMessageRow } from "../components/AnimatedMessageRow";

interface ChatMessage {
  id: string;
  sender: "user" | "coach";
  text: string;
  time: string;
  imageUri?: string;
  isLoggedMeal?: boolean;
}

const PROMPT_SUGGESTIONS = [
  "machi bulking ku enna sapdanum?",
  "how much protein should i eat?",
  "2 dosa calories?",
  "running panna muscle loss aguma?",
  "creatine daily edukanuma?",
  "I ate 3 eggs",
  "today enaku evlo calories venum?",
  "best workout for chest?",
  "night rice sapta weight increase aguma?",
  "pre-workout enna sapdanum?",
];

export default function NutritionCoachScreen() {
  const { user } = useAuth();
  const { colors } = useTheme();
  const router = useRouter();

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [attachedImageUri, setAttachedImageUri] = useState<string | null>(null);

  const targetCals = user?.daily_calorie_target || 2000;
  const targetProtein = user?.protein_target || (user?.weight_kg ? Math.round(user.weight_kg * 1.8) : 140);
  const userName = user?.name ? user.name.split(" ")[0] : "Friend";
  const userWeight = user?.weight_kg || 70;
  const userGoal = (user?.goal || "muscle gain").replace("_", " ");

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "1",
      sender: "coach",
      text: `Vanakkam ${userName}! 👋 I'm your dedicated FITBRO AI Fitness & Nutrition Coach.\n\n` +
        `📊 **Your Active Profile:**\n` +
        `• Weight: **${userWeight} kg** | Goal: **${userGoal.toUpperCase()}**\n` +
        `• Target: **${targetCals} kcal/day** | Protein: **${targetProtein}g**\n\n` +
        `Ask me anything in **English, Tamil, or Tanglish**! Try:\n` +
        `• *"machi bulking ku enna sapdanum?"*\n` +
        `• *"running panna muscle loss aguma?"*\n` +
        `• *"2 dosa calories?"*\n` +
        `• *"I ate 3 eggs"* (I'll automatically log it into your diary!)`,
      time: "Just now",
    },
  ]);

  const scrollViewRef = useRef<ScrollView>(null);

  const handlePickImage = async () => {
    try {
      const permission = await ImagePicker.requestMediaLibraryPermissionsAsync();
      if (!permission.granted) {
        Alert.alert(
          "Permission Required",
          "Please allow photo library access to share food images with your coach."
        );
        return;
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ["images"],
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        setAttachedImageUri(result.assets[0].uri);
      }
    } catch {
      Alert.alert("Notice", "Unable to select photo. You can type your food question directly.");
    }
  };

  const handleTakePhoto = async () => {
    try {
      const permission = await ImagePicker.requestCameraPermissionsAsync();
      if (!permission.granted) {
        Alert.alert(
          "Permission Required",
          "Please grant camera access to snap food for your coach."
        );
        return;
      }

      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ["images"],
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        setAttachedImageUri(result.assets[0].uri);
      }
    } catch {
      Alert.alert("Notice", "Unable to open camera.");
    }
  };

  const handleSend = async (textToSend?: string) => {
    const query = (textToSend || input).trim();
    const imageToAnalyze = attachedImageUri;

    if (!query && !imageToAnalyze) return;

    // Reset inputs
    setInput("");
    setAttachedImageUri(null);

    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      sender: "user",
      text: query || (imageToAnalyze ? "📸 Analyze this meal for me" : ""),
      time: "Now",
      imageUri: imageToAnalyze || undefined,
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    scrollViewRef.current?.scrollToEnd({ animated: true });

    try {
      if (imageToAnalyze) {
        // Image-based food analysis with coach
        const res = await coachService.analyzeFoodImageWithCoach(
          imageToAnalyze,
          "image/jpeg",
          query || "Analyze this food for me"
        );

        let coachText = res?.coach_commentary || "Here is your meal breakdown:";
        if (res?.meal_analysis) {
          const m = res.meal_analysis;
          coachText += `\n\n🍽️ **Estimated Nutrition:**\n` +
            `• Calories: **${m.total_calories || 0} kcal**\n` +
            `• Protein: **${m.total_protein_g || 0}g**\n` +
            `• Carbs: **${m.total_carbs_g || 0}g**\n` +
            `• Fats: **${m.total_fat_g || 0}g**`;
        }

        const coachMsg: ChatMessage = {
          id: (Date.now() + 1).toString(),
          sender: "coach",
          text: coachText,
          time: "Now",
          isLoggedMeal: true,
        };
        setMessages((prev) => [...prev, coachMsg]);
      } else {
        // Build conversation history for multi-turn context
        const convHistory: CoachChatMessage[] = messages.slice(-6).map((m) => ({
          role: m.sender === "user" ? "user" : "assistant",
          content: m.text,
        }));

        const res = await coachService.chatWithCoach(query, convHistory, true);

        const coachMsg: ChatMessage = {
          id: (Date.now() + 1).toString(),
          sender: "coach",
          text: res.reply,
          time: "Now",
          isLoggedMeal: Boolean(res.logged_meal),
        };
        setMessages((prev) => [...prev, coachMsg]);
      }
    } catch {
      // Offline fallback
      const offlineRes = coachService.generateOfflineResponse(query);
      const coachMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "coach",
        text: offlineRes.reply,
        time: "Now",
      };
      setMessages((prev) => [...prev, coachMsg]);
    } finally {
      setLoading(false);
      scrollViewRef.current?.scrollToEnd({ animated: true });
    }
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      {/* Top Header */}
      <View style={[styles.header, { borderBottomColor: colors.border }]}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()} activeOpacity={0.7}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <View style={styles.headerTitleWrap}>
          <Text style={[styles.headerTitle, { color: colors.text }]}>AI Fitness & Nutrition Coach</Text>
          <Text style={[styles.headerStatus, { color: "#10B981" }]}>Online • Pro Intelligence (Tamil & English)</Text>
        </View>
        <View style={[styles.vipPill, { backgroundColor: `${colors.amber}20` }]}>
          <Ionicons name="sparkles" size={12} color={colors.amber} />
          <Text style={[styles.vipPillText, { color: colors.amber }]}>FITBRO AI</Text>
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
              <AnimatedMessageRow key={m.id} isNew={m.time === "Now"}>
                <View
                  style={[
                    styles.messageBubbleWrap,
                    isUser ? styles.userBubbleWrap : styles.coachBubbleWrap,
                  ]}
                >
                  {!isUser && (
                    <View style={[styles.coachAvatar, { backgroundColor: `${colors.primary}20` }]}>
                      <Ionicons name="barbell" size={18} color={colors.primary} />
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
                    {m.imageUri && (
                      <Image
                        source={{ uri: m.imageUri }}
                        style={styles.messageImage}
                        resizeMode="cover"
                      />
                    )}
                    {m.isLoggedMeal && (
                      <View style={styles.mealBadge}>
                        <Ionicons name="checkmark-circle" size={14} color="#10B981" />
                        <Text style={styles.mealBadgeText}>Food Logged into Diary</Text>
                      </View>
                    )}
                    <Text
                      style={[
                        styles.bubbleText,
                        { color: isUser ? "#FFFFFF" : colors.text },
                      ]}
                    >
                      {m.text}
                    </Text>
                    <Text
                      style={[
                        styles.timestampText,
                        { color: isUser ? "rgba(255,255,255,0.7)" : colors.textMuted },
                      ]}
                    >
                      {m.time}
                    </Text>
                  </View>
                </View>
              </AnimatedMessageRow>
            );
          })}

          {loading && (
            <AnimatedMessageRow isNew={true}>
              <View style={[styles.messageBubbleWrap, styles.coachBubbleWrap]}>
                <View style={[styles.coachAvatar, { backgroundColor: `${colors.primary}20` }]}>
                  <Ionicons name="barbell" size={18} color={colors.primary} />
                </View>
                <View
                  style={[
                    styles.bubble,
                    styles.coachBubble,
                    {
                      backgroundColor: colors.surface,
                      borderColor: colors.border,
                      flexDirection: "row",
                      alignItems: "center",
                      gap: 8,
                      paddingVertical: 12,
                      paddingHorizontal: 16,
                    },
                  ]}
                >
                  <TypingDots color={colors.primary} size={7} />
                  <Text style={[styles.bubbleText, { color: colors.textSecondary, fontSize: 13 }]}>
                    Coach is thinking...
                  </Text>
                </View>
              </View>
            </AnimatedMessageRow>
          )}
        </ScrollView>

        {/* Suggestion Chips */}
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

        {/* Attached Photo Preview Bar */}
        {attachedImageUri && (
          <View style={[styles.previewBar, { backgroundColor: colors.surfaceHighlight, borderColor: colors.border }]}>
            <Image source={{ uri: attachedImageUri }} style={styles.previewThumbnail} />
            <Text style={[styles.previewText, { color: colors.text }]}>Photo ready to analyze</Text>
            <TouchableOpacity onPress={() => setAttachedImageUri(null)} style={styles.previewCloseBtn}>
              <Ionicons name="close-circle" size={20} color={colors.textMuted} />
            </TouchableOpacity>
          </View>
        )}

        {/* Input Bar */}
        <View style={[styles.inputBar, { backgroundColor: colors.surface, borderTopColor: colors.border }]}>
          <TouchableOpacity
            style={styles.mediaBtn}
            onPress={handlePickImage}
            activeOpacity={0.7}
          >
            <Ionicons name="images-outline" size={22} color={colors.textSecondary} />
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.mediaBtn}
            onPress={handleTakePhoto}
            activeOpacity={0.7}
          >
            <Ionicons name="camera-outline" size={22} color={colors.textSecondary} />
          </TouchableOpacity>

          <TextInput
            style={[
              styles.textInput,
              { backgroundColor: colors.surfaceHighlight, color: colors.text, borderColor: colors.border },
            ]}
            placeholder="Ask coach or type 'I ate 3 eggs'..."
            placeholderTextColor={colors.textMuted}
            value={input}
            onChangeText={setInput}
            onSubmitEditing={() => handleSend()}
            returnKeyType="send"
          />

          <TouchableOpacity
            style={[
              styles.sendButton,
              { backgroundColor: input.trim() || attachedImageUri ? colors.primary : `${colors.primary}60` },
            ]}
            onPress={() => handleSend()}
            disabled={!input.trim() && !attachedImageUri}
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
    maxWidth: "88%",
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
    minWidth: 80,
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
  timestampText: {
    fontSize: 10,
    marginTop: 4,
    alignSelf: "flex-end",
  },
  messageImage: {
    width: 220,
    height: 150,
    borderRadius: 12,
    marginBottom: 8,
  },
  mealBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    backgroundColor: "rgba(16, 185, 129, 0.15)",
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
    alignSelf: "flex-start",
    marginBottom: 6,
  },
  mealBadgeText: {
    fontSize: 11,
    fontWeight: "700",
    color: "#10B981",
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
  previewBar: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderTopWidth: 1,
    gap: 10,
  },
  previewThumbnail: {
    width: 36,
    height: 36,
    borderRadius: 6,
  },
  previewText: {
    flex: 1,
    fontSize: 13,
    fontWeight: "600",
  },
  previewCloseBtn: {
    padding: 4,
  },
  inputBar: {
    flexDirection: "row",
    alignItems: "center",
    paddingHorizontal: 10,
    paddingVertical: 10,
    borderTopWidth: 1,
    gap: 8,
  },
  mediaBtn: {
    padding: 6,
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
