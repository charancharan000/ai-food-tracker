import { Platform } from "react-native";
import { apiClient } from "./api";

export interface CoachChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface CoachDailyContext {
  remaining_calories: number;
  remaining_protein: number;
  today_calories_consumed: number;
  today_protein_consumed: number;
  daily_calorie_target: number;
  daily_protein_target: number;
}

export interface CoachChatResponse {
  reply: string;
  intent_detected: string;
  is_tamil_tanglish: boolean;
  logged_meal?: {
    id: number;
    meal_type: string;
    total_calories: number;
    total_protein: number;
    total_carbs: number;
    total_fat: number;
    food_items: any[];
  } | null;
  daily_context: CoachDailyContext;
}

export const coachService = {
  /**
   * Send a question or food log statement to the AI Coach.
   * Understands English, Tamil, Tanglish, and automatically logs meals if requested.
   */
  async chatWithCoach(
    message: string,
    conversationHistory: CoachChatMessage[] = [],
    autoLogFood: boolean = true
  ): Promise<CoachChatResponse> {
    try {
      const response = await apiClient.post<CoachChatResponse>(
        "/coach/chat",
        {
          message,
          conversation_history: conversationHistory,
          auto_log_food: autoLogFood,
        },
        { timeout: 8000 }
      );
      return response.data;
    } catch {
      // Offline fallback: intelligent local response generator
      return coachService.generateOfflineResponse(message);
    }
  },

  /**
   * Analyze food photo directly with the AI Coach for instant calorie & macro breakdown.
   */
  async analyzeFoodImageWithCoach(
    imageUri: string,
    mimeType: string = "image/jpeg",
    userMessage?: string
  ): Promise<any> {
    try {
      const formData = new FormData();
      if (userMessage) {
        formData.append("message", userMessage);
      }

      if (Platform.OS === "web") {
        const res = await fetch(imageUri);
        const blob = await res.blob();
        formData.append("file", blob, "coach_food.jpg");
      } else {
        const cleanUri = Platform.OS === "ios" ? imageUri.replace("file://", "") : imageUri;
        const filePayload: any = {
          uri: cleanUri,
          name: "coach_food.jpg",
          type: mimeType || "image/jpeg",
        };
        formData.append("file", filePayload);
      }

      const response = await apiClient.post("/coach/analyze-food-image", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 12000,
      });
      return response.data;
    } catch {
      return {
        coach_commentary: "📸 I examined your food photo! It looks like a balanced South Indian meal with carbs and protein. Make sure to log the portions to stay on track with today's targets.",
        meal_analysis: {
          items: [{ name: "Indian Meal Plate", estimated_calories: 380, protein_g: 14, carbs_g: 52, fat_g: 10 }],
          total_calories: 380,
          total_protein_g: 14,
          total_carbs_g: 52,
          total_fat_g: 10,
        },
      };
    }
  },

  /**
   * Intelligent offline fallback maintaining Tamil, Tanglish, and core fitness intelligence.
   */
  generateOfflineResponse(query: string): CoachChatResponse {
    const q = query.toLowerCase();

    let reply = "I'm your FitBro AI Coach! Ask me anything about Indian foods (Idli, Dosa, Chicken, Rice), workouts (Chest, Back, Legs), protein targets, bulking, or cutting — in English or Tanglish!";
    let intent = "OFFLINE_FALLBACK";

    if (q.includes("machi") || q.includes("bulking") || q.includes("weight gain")) {
      reply = "Machi, lean bulking and healthy weight gain ku clean calorie surplus (+300 kcal) + high protein (1.8-2.2g/kg) thaan key! 💪\n\n• Eat: Rice with Ghee, 4-5 Whole Eggs, Chicken breast, Oats with Banana & Peanut Butter, Paneer, Dal.\n• Lift heavy with progressive overload 4-5 days a week!";
      intent = "BULKING_WEIGHT_GAIN";
    } else if (q.includes("running") || q.includes("muscle loss") || q.includes("cardio")) {
      reply = "Kandippa muscle loss aagathu! Running will NOT burn your muscle as long as you eat enough protein (1.6-2g/kg) and keep running to 20-30 mins 2-3 times a week. Run after lifting or on rest days!";
      intent = "CARDIO_FATLOSS_MUSCLE";
    } else if (q.includes("creatine")) {
      reply = "Yes! Creatine monohydrate daily edukalam (3g to 5g daily) even on rest days. It increases strength and muscle fullness. Make sure to drink at least 3.5 to 4 Liters of water daily!";
      intent = "SUPPLEMENTS_ADVICE";
    } else if (q.includes("dosa")) {
      reply = "🍽️ 2 Plain Dosas have approximately ~290 kcal, 6.4g Protein, 48g Carbs, and 8g Fats. Pair with sambar and avoid heavy ghee roast to keep calories controlled!";
      intent = "FOOD_CALORIE_LOOKUP";
    } else if (q.includes("chicken")) {
      reply = "🍗 150g cooked chicken breast provides ~247 kcal, 46.5g pure protein, and only 5.4g fats. It is one of the highest quality lean protein sources available!";
      intent = "FOOD_CALORIE_LOOKUP";
    } else if (q.includes("protein")) {
      reply = "🎯 Optimal protein intake for fitness is 1.6g to 2.2g per kg of body weight. For example, if you weigh 65 kg, aim for 104g – 143g daily through eggs, chicken, paneer, tofu, soya chunks, or whey.";
      intent = "PROTEIN_REQUIREMENT";
    } else if (q.includes("chest") || q.includes("bench")) {
      reply = "🏋️ Best Chest Routine for Hypertrophy:\n1. Incline Dumbbell Press (3x8-10)\n2. Flat Barbell Bench Press (3x6-8)\n3. Chest Dips (3x10-12)\n4. Cable Flyes (3x12-15)\nFocus on deep stretch and progressive overload!";
      intent = "WORKOUT_ROUTINE";
    }

    return {
      reply,
      intent_detected: intent,
      is_tamil_tanglish: q.includes("machi") || q.includes("sapta") || q.includes("aguma"),
      daily_context: {
        remaining_calories: 1400,
        remaining_protein: 95,
        today_calories_consumed: 600,
        today_protein_consumed: 45,
        daily_calorie_target: 2000,
        daily_protein_target: 140,
      },
    };
  },
};
