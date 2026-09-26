import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Linking,
  Alert,
  Platform,
} from "react-native";
import { useRouter } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useTheme } from "../hooks/useTheme";

const SUPPORT_EMAIL = "codewithsan0607@gmail.com";

interface FaqItem {
  id: string;
  question: string;
  answer: string;
}

const FAQS: FaqItem[] = [
  {
    id: "1",
    question: "How does the AI Food Scanner work?",
    answer:
      "NutriScan AI uses deep computer vision to identify foods on your plate, approximate portion sizes in grams, and calculate total calories, protein, carbs, and fats instantly.",
  },
  {
    id: "2",
    question: "Can I use NutriScan AI completely offline?",
    answer:
      "Yes! NutriScan AI features an offline-first architecture. You can register, log meals, track daily water intake, view macros, and browse past history even without internet access.",
  },
  {
    id: "3",
    question: "What is included with Pro Membership?",
    answer:
      "Pro members unlock the AI Smart Meal Planner, custom recipe generation, AI Nutrition Coach chatbot, in-depth micronutrient analytics, and unlimited priority photo scans.",
  },
  {
    id: "4",
    question: "How are my daily calorie & macro targets calculated?",
    answer:
      "Targets are calculated using the Mifflin-St Jeor formula based on your age, biological sex, height, weight, activity level, and fitness goal (lose, maintain, or gain).",
  },
  {
    id: "5",
    question: "How can I contact developer support?",
    answer:
      "You can send an email directly to codewithsan0607@gmail.com anytime. We typically respond within 24 hours.",
  },
];

export default function SupportCenterScreen() {
  const { colors } = useTheme();
  const router = useRouter();

  const [expandedFaq, setExpandedFaq] = useState<string | null>("1");
  const [subject, setSubject] = useState("");
  const [message, setMessage] = useState("");

  const handleOpenEmail = (customSubject?: string, customBody?: string) => {
    const sub = encodeURIComponent(customSubject || "NutriScan AI Support Inquiry");
    const body = encodeURIComponent(
      (customBody || "Hello Support Team,\n\nI need assistance with...") +
        `\n\n[App Version: 1.0.2 | Platform: ${Platform.OS}]`
    );
    const url = `mailto:${SUPPORT_EMAIL}?subject=${sub}&body=${body}`;

    Linking.canOpenURL(url)
      .then((supported) => {
        if (supported) {
          Linking.openURL(url);
        } else {
          Alert.alert(
            "Contact Email",
            `Please write to our support team directly at:\n\n${SUPPORT_EMAIL}`,
            [{ text: "OK" }]
          );
        }
      })
      .catch(() => {
        Alert.alert("Contact Email", `Support email: ${SUPPORT_EMAIL}`);
      });
  };

  const handleSendForm = () => {
    if (!message.trim()) {
      Alert.alert("Missing Message", "Please type your message before sending.");
      return;
    }
    handleOpenEmail(subject.trim() || "NutriScan AI User Feedback", message.trim());
    setSubject("");
    setMessage("");
  };

  const toggleFaq = (id: string) => {
    setExpandedFaq(expandedFaq === id ? null : id);
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]} edges={["top"]}>
      <View style={[styles.header, { borderBottomColor: colors.border }]}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()} activeOpacity={0.7}>
          <Ionicons name="arrow-back" size={24} color={colors.text} />
        </TouchableOpacity>
        <Text style={[styles.headerTitle, { color: colors.text }]}>Support Center</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
        <View style={[styles.heroCard, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <View style={[styles.heroIconCircle, { backgroundColor: `${colors.primary}20` }]}>
            <Ionicons name="headset" size={32} color={colors.primary} />
          </View>
          <Text style={[styles.heroTitle, { color: colors.text }]}>We are here to help</Text>
          <Text style={[styles.heroSubtitle, { color: colors.textSecondary }]}>
            Have questions, feedback, or need help? Reach out directly to our dedicated support desk.
          </Text>

          <View style={[styles.emailBadge, { backgroundColor: colors.surfaceHighlight }]}>
            <Ionicons name="mail" size={16} color={colors.primary} />
            <Text style={[styles.emailBadgeText, { color: colors.text }]}>{SUPPORT_EMAIL}</Text>
          </View>

          <TouchableOpacity
            style={[styles.primaryActionBtn, { backgroundColor: colors.primary }]}
            onPress={() => handleOpenEmail()}
            activeOpacity={0.8}
          >
            <Ionicons name="paper-plane" size={18} color="#FFFFFF" />
            <Text style={styles.primaryActionBtnText}>Email Support Desk</Text>
          </TouchableOpacity>
        </View>

        <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>Quick Message</Text>
          <Text style={[styles.sectionSubtitle, { color: colors.textSecondary }]}>
            Draft your inquiry here and it will open directly in your mail app.
          </Text>

          <View style={styles.formGroup}>
            <Text style={[styles.inputLabel, { color: colors.textSecondary }]}>SUBJECT</Text>
            <TextInput
              style={[
                styles.textInput,
                { backgroundColor: colors.surfaceHighlight, color: colors.text, borderColor: colors.border },
              ]}
              placeholder="e.g., Question about meal targets"
              placeholderTextColor={colors.textMuted}
              value={subject}
              onChangeText={setSubject}
            />
          </View>

          <View style={styles.formGroup}>
            <Text style={[styles.inputLabel, { color: colors.textSecondary }]}>MESSAGE</Text>
            <TextInput
              style={[
                styles.textArea,
                { backgroundColor: colors.surfaceHighlight, color: colors.text, borderColor: colors.border },
              ]}
              placeholder="Describe what you need assistance with..."
              placeholderTextColor={colors.textMuted}
              multiline
              numberOfLines={4}
              textAlignVertical="top"
              value={message}
              onChangeText={setMessage}
            />
          </View>

          <TouchableOpacity
            style={[styles.sendBtn, { backgroundColor: colors.primary }]}
            onPress={handleSendForm}
            activeOpacity={0.8}
          >
            <Ionicons name="send" size={16} color="#FFFFFF" />
            <Text style={styles.sendBtnText}>Compose Inquiry</Text>
          </TouchableOpacity>
        </View>

        <View style={[styles.card, { backgroundColor: colors.surface, borderColor: colors.border }]}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>Frequently Asked Questions</Text>

          <View style={styles.faqList}>
            {FAQS.map((faq) => {
              const isOpen = expandedFaq === faq.id;
              return (
                <View
                  key={faq.id}
                  style={[
                    styles.faqItem,
                    { borderColor: colors.border, backgroundColor: isOpen ? colors.surfaceHighlight : "transparent" },
                  ]}
                >
                  <TouchableOpacity
                    style={styles.faqQuestionRow}
                    onPress={() => toggleFaq(faq.id)}
                    activeOpacity={0.7}
                  >
                    <Text style={[styles.faqQuestion, { color: colors.text }]}>{faq.question}</Text>
                    <Ionicons
                      name={isOpen ? "chevron-up" : "chevron-down"}
                      size={18}
                      color={colors.textMuted}
                    />
                  </TouchableOpacity>
                  {isOpen && (
                    <Text style={[styles.faqAnswer, { color: colors.textSecondary }]}>{faq.answer}</Text>
                  )}
                </View>
              );
            })}
          </View>
        </View>

        <View style={styles.footerNote}>
          <Text style={[styles.footerText, { color: colors.textMuted }]}>
            NutriScan AI v1.0.2 • Support Desk: codewithsan0607@gmail.com
          </Text>
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
  heroCard: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 20,
    alignItems: "center",
  },
  heroIconCircle: {
    width: 64,
    height: 64,
    borderRadius: 32,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 12,
  },
  heroTitle: {
    fontSize: 20,
    fontWeight: "800",
    marginBottom: 6,
  },
  heroSubtitle: {
    fontSize: 14,
    textAlign: "center",
    lineHeight: 20,
    marginBottom: 16,
    paddingHorizontal: 8,
  },
  emailBadge: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 12,
    marginBottom: 16,
  },
  emailBadgeText: {
    fontSize: 14,
    fontWeight: "700",
  },
  primaryActionBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    width: "100%",
    height: 48,
    borderRadius: 14,
  },
  primaryActionBtnText: {
    color: "#FFFFFF",
    fontSize: 15,
    fontWeight: "700",
  },
  card: {
    borderRadius: 20,
    borderWidth: 1,
    padding: 18,
  },
  sectionTitle: {
    fontSize: 17,
    fontWeight: "800",
    marginBottom: 4,
  },
  sectionSubtitle: {
    fontSize: 13,
    marginBottom: 14,
  },
  formGroup: {
    marginBottom: 12,
  },
  inputLabel: {
    fontSize: 11,
    fontWeight: "700",
    letterSpacing: 0.5,
    marginBottom: 6,
  },
  textInput: {
    height: 46,
    borderRadius: 12,
    borderWidth: 1,
    paddingHorizontal: 12,
    fontSize: 14,
  },
  textArea: {
    height: 90,
    borderRadius: 12,
    borderWidth: 1,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
  },
  sendBtn: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    height: 46,
    borderRadius: 12,
    marginTop: 4,
  },
  sendBtnText: {
    color: "#FFFFFF",
    fontSize: 15,
    fontWeight: "700",
  },
  faqList: {
    gap: 10,
    marginTop: 8,
  },
  faqItem: {
    borderRadius: 12,
    borderWidth: 1,
    padding: 12,
  },
  faqQuestionRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  faqQuestion: {
    fontSize: 14,
    fontWeight: "700",
    flex: 1,
    marginRight: 8,
  },
  faqAnswer: {
    fontSize: 13,
    lineHeight: 18,
    marginTop: 8,
  },
  footerNote: {
    alignItems: "center",
    marginTop: 8,
  },
  footerText: {
    fontSize: 12,
  },
});
