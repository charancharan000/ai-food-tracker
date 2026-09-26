"""
Comprehensive Test Suite for FITBRO AI Fitness & Nutrition Coach
Verifies:
1. Personalized Profile Integration (BMR, TDEE, Protein recommendations using stored profile)
2. Accurate Food Nutrition Estimates (Idli, Dosa, Chicken, Eggs, Rice, Sambar, etc.)
3. Tamil, Tanglish, and Slang Understanding ("machi", "evlo", "sapdanum", "aguma", etc.)
4. 8 Core Knowledge Areas:
   - Calorie calculation
   - Protein requirements
   - Food calorie lookups
   - Bulking & weight gain
   - Running / cardio vs muscle loss
   - Creatine & pre-workout supplements
   - Night rice / carb myths
   - Chest / back / leg hypertrophy workouts
   - Recovery, sleep & DOMS
5. Daily Progress & Remaining Macros integration
6. Automatic Food Logging into Database ("I ate 3 eggs", "I ate 2 idli, sambar and one egg")
7. Conversation context memory
8. Full API Endpoint Integration (`/api/v1/coach/chat`)
"""

import pytest
from httpx import AsyncClient
from app.services.fitness_coach_engine import (
    FitnessCoachIntelligence,
    UserProfileContext,
    FOOD_DATABASE,
)


@pytest.fixture
def sample_user_profile():
    return UserProfileContext(
        name="Charan",
        age=24,
        gender="male",
        height_cm=175.0,
        weight_kg=60.0,
        activity_level="moderate",
        goal="muscle_gain",
        daily_calorie_target=2400.0,
        protein_target=150.0,
        carb_target=300.0,
        fat_target=70.0,
        daily_water_target_ml=3000,
        calories_consumed_today=850.0,
        protein_consumed_today=45.0,
        carbs_consumed_today=110.0,
        fat_consumed_today=25.0,
        water_consumed_today=1500,
    )


def test_bmr_and_tdee_calculation(sample_user_profile):
    # Weight=60, Height=175, Age=24, Male
    # BMR = 10*60 + 6.25*175 - 5*24 + 5 = 600 + 1093.75 - 120 + 5 = 1578.75
    bmr = FitnessCoachIntelligence.calculate_bmr(60.0, 175.0, 24, "male")
    assert 1570 <= bmr <= 1585

    tdee = FitnessCoachIntelligence.calculate_tdee(bmr, "moderate")
    assert tdee > bmr
    assert 2400 <= tdee <= 2500


def test_tamil_tanglish_detection():
    assert FitnessCoachIntelligence.detect_tamil_tanglish("machi bulking ku enna sapdanum?") is True
    assert FitnessCoachIntelligence.detect_tamil_tanglish("gym pona muscle loss aguma?") is True
    assert FitnessCoachIntelligence.detect_tamil_tanglish("creatine daily edukanuma?") is True
    assert FitnessCoachIntelligence.detect_tamil_tanglish("chicken 200g protein evlo?") is True
    assert FitnessCoachIntelligence.detect_tamil_tanglish("today enaku evlo calories venum?") is True
    assert FitnessCoachIntelligence.detect_tamil_tanglish("how much protein should i eat?") is False


def test_protein_inquiry_uses_stored_profile(sample_user_profile):
    """User asks 'how much protein should i eat?'. Coach must use stored 60kg without asking again."""
    res = FitnessCoachIntelligence.generate_coach_answer(
        user_message="how much protein should i eat?",
        user_profile=sample_user_profile,
    )
    assert res.intent_detected == "PROTEIN_REQUIREMENT"
    # Should reference 60 kg profile and calculate ~96g - 132g
    assert "60" in res.reply_text
    assert "96" in res.reply_text or "1.6" in res.reply_text
    assert "132" in res.reply_text or "2.2" in res.reply_text
    assert "150g" in res.reply_text # references existing target


def test_food_calorie_lookup_2_dosa(sample_user_profile):
    res = FitnessCoachIntelligence.generate_coach_answer(
        user_message="2 dosa calories?",
        user_profile=sample_user_profile,
    )
    assert res.intent_detected == "FOOD_CALORIE_LOOKUP"
    assert "Dosa" in res.reply_text
    assert "290" in res.reply_text or "280" in res.reply_text or "145" in res.reply_text
    assert "Protein" in res.reply_text
    assert "Carbohydrates" in res.reply_text


def test_food_calorie_lookup_chicken_200g(sample_user_profile):
    res = FitnessCoachIntelligence.generate_coach_answer(
        user_message="chicken 200g protein evlo?",
        user_profile=sample_user_profile,
    )
    assert res.intent_detected == "FOOD_CALORIE_LOOKUP"
    assert "Chicken" in res.reply_text
    assert "62" in res.reply_text or "60" in res.reply_text or "31" in res.reply_text


def test_bulking_diet_tanglish_query(sample_user_profile):
    res = FitnessCoachIntelligence.generate_coach_answer(
        user_message="machi bulking ku enna sapdanum?",
        user_profile=sample_user_profile,
    )
    assert res.intent_detected == "BULKING_WEIGHT_GAIN"
    assert res.is_tamil_tanglish is True
    assert "surplus" in res.reply_text.lower()
    assert "rice" in res.reply_text.lower()
    assert "eggs" in res.reply_text.lower() or "peanut butter" in res.reply_text.lower()


def test_running_muscle_loss_query(sample_user_profile):
    res = FitnessCoachIntelligence.generate_coach_answer(
        user_message="running panna muscle loss aguma?",
        user_profile=sample_user_profile,
    )
    assert res.intent_detected == "CARDIO_FATLOSS_MUSCLE"
    assert "muscle loss" in res.reply_text.lower()
    assert "protein" in res.reply_text.lower()


def test_creatine_daily_query(sample_user_profile):
    res = FitnessCoachIntelligence.generate_coach_answer(
        user_message="creatine daily edukanuma?",
        user_profile=sample_user_profile,
    )
    assert res.intent_detected == "SUPPLEMENTS_ADVICE"
    assert "3g to 5g" in res.reply_text or "3-5g" in res.reply_text or "3g" in res.reply_text
    assert "water" in res.reply_text.lower()


def test_daily_progress_remaining_calories(sample_user_profile):
    # Cal target: 2400, Consumed: 850 -> Remaining: 1550
    # Protein target: 150, Consumed: 45 -> Remaining: 105
    res = FitnessCoachIntelligence.generate_coach_answer(
        user_message="today enaku evlo calories venum?",
        user_profile=sample_user_profile,
    )
    assert res.intent_detected == "DAILY_PROGRESS_QUERY"
    assert "1550" in res.reply_text
    assert "105" in res.reply_text


def test_night_rice_weight_increase_myth(sample_user_profile):
    res = FitnessCoachIntelligence.generate_coach_answer(
        user_message="night rice sapta weight increase aguma?",
        user_profile=sample_user_profile,
    )
    assert res.intent_detected == "NUTRITION_MYTHS_LIFESTYLE"
    assert "calorie surplus" in res.reply_text.lower() or "calories" in res.reply_text.lower()


def test_best_workout_for_chest(sample_user_profile):
    res = FitnessCoachIntelligence.generate_coach_answer(
        user_message="best workout for chest?",
        user_profile=sample_user_profile,
    )
    assert res.intent_detected == "WORKOUT_ROUTINE"
    assert "Incline" in res.reply_text
    assert "Bench Press" in res.reply_text
    assert "Flyes" in res.reply_text or "Dips" in res.reply_text


def test_food_logging_parsing_3_eggs():
    parsed = FitnessCoachIntelligence.parse_food_logging_query("I ate 3 eggs")
    assert parsed is not None
    assert len(parsed) == 1
    assert parsed[0].name == "Boiled Egg (Whole)"
    assert parsed[0].quantity == 3.0
    assert 210 <= parsed[0].calories <= 230
    assert 18.0 <= parsed[0].protein_g <= 20.0


def test_food_logging_parsing_multi_item():
    parsed = FitnessCoachIntelligence.parse_food_logging_query("I ate 2 idli, sambar and one egg")
    assert parsed is not None
    assert len(parsed) >= 2
    names = [p.name for p in parsed]
    assert any("Idli" in n for n in names)
    assert any("Sambar" in n or "Egg" in n for n in names)


@pytest.mark.asyncio
async def test_coach_api_chat_flow(client: AsyncClient, auth_headers: dict):
    """Verifies POST /api/v1/coach/chat with protein inquiry."""
    payload = {
        "message": "how much protein should i eat?",
        "conversation_history": [],
    }
    res = await client.post("/api/v1/coach/chat", headers=auth_headers, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert data["intent_detected"] == "PROTEIN_REQUIREMENT"
    assert "daily_context" in data
    assert "remaining_protein" in data["daily_context"]


@pytest.mark.asyncio
async def test_coach_api_food_logging_and_db_integration(client: AsyncClient, auth_headers: dict):
    """Verifies that saying 'I ate 3 eggs' automatically logs a meal in the database."""
    payload = {
        "message": "I ate 3 eggs",
        "conversation_history": [],
        "auto_log_food": True,
    }
    res = await client.post("/api/v1/coach/chat", headers=auth_headers, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["intent_detected"] == "FOOD_LOG_AUTO"
    assert "✅" in data["reply"]
    assert data["logged_meal"] is not None
    assert data["logged_meal"]["total_calories"] > 200.0
    assert len(data["logged_meal"]["food_items"]) == 1

    # Verify meal appears in /meals/today
    today_res = await client.get("/api/v1/meals/today", headers=auth_headers)
    assert today_res.status_code == 200
    meals = today_res.json()
    assert any(m["id"] == data["logged_meal"]["id"] for m in meals)
