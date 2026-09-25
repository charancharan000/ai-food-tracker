# AI Food Tracker

A full-stack mobile application that tracks meals, calories, and macronutrients from food photos using vision models. Built with React Native (Expo) and FastAPI.

## Features

- **Photo Meal Recognition**: Snap or upload a photo to detect food items, estimated weight in grams, and complete macro breakdown (calories, protein, carbs, fat, fiber).
- **Portion Adjustments**: Fine-tune grams or servings with real-time recalculation.
- **Daily Dashboard**: Visual calorie ring, macro target bars, hydration tracker, and grouped meal logs (Breakfast, Lunch, Snack, Dinner).
- **Biometric Calculations**: Mifflin-St Jeor equation calculates personalized BMR, TDEE, and macro goals from user profile.
- **Theme Studio**: 4 color themes (Cyber Violet, Sunset Coral, Ocean Cobalt, Neon Emerald) with Dark/Light modes.

## Tech Stack

- **Mobile**: React Native, Expo SDK 57, Expo Router, TypeScript, React Native SVG
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy (async), SQLite / PostgreSQL, Pydantic v2
- **Vision Models**: Google Gemini / OpenAI vision models with deterministic fallback

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API documentation will be available at `http://localhost:8000/docs`.

### 2. Mobile App

```bash
cd mobile
npm install
npx expo start
```

Open the Expo Go app on your physical device and scan the terminal QR code, or press:
- `a` to launch Android emulator
- `i` to launch iOS simulator
- `w` to run web preview

## Configuration

### Backend (`backend/.env`)

```env
SECRET_KEY=generate_a_random_secret_key_here
DATABASE_URL=sqlite+aiosqlite:///./nutriscan.db
AI_PROVIDER=gemini
AI_API_KEY=your_gemini_or_openai_api_key
AI_MODEL=gemini-2.0-flash
```

## Testing

```bash
# Run backend tests
cd backend
pytest

# Run mobile tests
cd mobile
npm test
```

## License

MIT
