# AI Food Tracker 🥗📱
> Full-Stack Mobile AI Food & Nutrition Tracking Application (NutriScan AI)

NutriScan AI is a full-stack mobile application that empowers users to take a photo of their meal or upload a food image. The backend multimodal Vision AI identifies distinct food items, estimates portion weights, calculates calorie and macronutrient breakdown (Protein, Carbs, Fat, Fiber, Sugar, Sodium), and logs the meal into the user's daily nutrition dashboard.

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [System Requirements](#3-system-requirements)
4. [Installation](#4-installation)
5. [Backend Setup](#5-backend-setup)
6. [Database Setup & Migrations](#6-database-setup--migrations)
7. [Environment Variables](#7-environment-variables)
8. [AI Vision API Configuration](#8-ai-vision-api-configuration)
9. [Mobile App Setup](#9-mobile-app-setup)
10. [Android Development](#10-android-development)
11. [iOS Development](#11-ios-development)
12. [API Documentation](#12-api-documentation)
13. [Running Tests](#13-running-tests)
14. [Production Deployment](#14-production-deployment)

---

## 1. Project Overview

NutriScan AI bridges cutting-edge computer vision with sports nutrition science:
- **Vision-Driven Logging**: Snap a photo of a single dish or mixed plate (e.g., Rice, Chicken Curry, Dal, Salad). The AI detects each item with high granularity.
- **Dynamic Portion Scaling**: Gram steppers (`[-] 350 g [+]`), serving multipliers, and presets (Small, Medium, Large) dynamically recalculate nutrition proportionally without making unnecessary AI round-trips.
- **Comprehensive Daily Dashboard**: Circular calorie ring, macro target bars (Protein, Carbs, Fat), meal breakdown (Breakfast, Lunch, Snack, Dinner), and one-tap water logging.
- **Biometric Health Profiles**: Mifflin-St Jeor BMR & TDEE formulas calculate tailored calorie targets based on Age, Gender, Height, Weight, Activity Level, and Fitness Goal (Lose Weight, Maintain, Gain Weight), with custom overrides.
- **Cross-Platform Experience**: Built with React Native & Expo Router with dark mode and light mode support.

---

## 2. Architecture

```
nutriscan-ai/
├── mobile/                           # React Native / Expo Frontend
│   ├── app/                          # Expo Router File-based Navigation
│   │   ├── _layout.tsx               # Root Layout with Theme & Auth Contexts
│   │   ├── index.tsx                 # Splash & Session Gate
│   │   ├── (auth)/                   # Authentication Group
│   │   │   ├── onboarding.tsx        # 3-Step Interactive Onboarding
│   │   │   ├── login.tsx             # Login with Demo Account feature
│   │   │   ├── register.tsx          # Account Registration
│   │   │   └── profile-setup.tsx     # Biometrics & Calorie Goal Engine
│   │   ├── (tabs)/                   # Bottom Tab Navigation
│   │   │   ├── _layout.tsx           # Floating Scan Button Tab Bar
│   │   │   ├── index.tsx             # Home Dashboard & Rings
│   │   │   ├── scan.tsx              # Camera/Gallery Scanner & AI Analysis
│   │   │   ├── history.tsx           # Food Log & Nutrition Charts
│   │   │   └── profile.tsx           # Goals, Settings & Theme Toggle
│   │   ├── meal/[id].tsx             # Meal Details & Portion Editor
│   │   └── water.tsx                 # Dedicated Hydration Tracker
│   ├── components/                   # Reusable Modern Mobile UI Components
│   │   ├── MacroRing.tsx             # SVG Circular Calorie Progress Ring
│   │   ├── MacroCard.tsx             # Protein / Carbs / Fat Progress Cards
│   │   ├── MealCard.tsx              # Grouped Meal Display (Breakfast/Lunch/etc.)
│   │   ├── PortionEditor.tsx         # Gram Steppers & Preset Multipliers
│   │   ├── AnalysisLoadingModal.tsx  # Multi-step AI Progress Modal
│   │   ├── FoodItemCard.tsx          # Detected Food Card with Confidence Tag
│   │   ├── WaterTrackerCard.tsx      # +250ml / +500ml Hydration Widget
│   │   ├── NutritionSummaryBar.tsx   # Compact Macros Summary Bar
│   │   └── ThemeToggle.tsx           # Dark/Light Mode Switcher
│   ├── services/                     # HTTP API Client & Endpoint Wrappers
│   ├── hooks/                        # useAuth and useTheme Hooks
│   ├── utils/                        # Nutrition Calculations & Storage
│   └── types/                        # TypeScript Interfaces
│
├── backend/                          # FastAPI REST API Backend
│   ├── app/
│   │   ├── api/v1/                   # REST Endpoints
│   │   │   ├── auth.py               # Register, Login, Me
│   │   │   ├── food.py               # Multipart Photo Upload & AI Analysis
│   │   │   ├── meals.py              # Full Meal CRUD
│   │   │   ├── dashboard.py          # Today's Progress & Historical Summary
│   │   │   ├── profile.py            # Anthropometrics & Target Goals
│   │   │   └── water.py              # Water Intake Logging
│   │   ├── core/                     # Config, JWT Security, Custom Exceptions
│   │   ├── db/                       # Async SQLAlchemy Session & Initializer
│   │   ├── models/                   # SQLAlchemy Models (User, Meal, FoodItem, WaterLog)
│   │   ├── schemas/                  # Pydantic v2 Models & Response Schemas
│   │   ├── services/                 # AI Vision Service & Nutrition Mathematics
│   │   └── utils/                    # Pillow Image Processing & Validation
│   ├── migrations/                   # Alembic Async Migrations
│   ├── tests/                        # 17 Pytest Test Cases (100% Passing)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── docker-compose.yml                # Multi-container PostgreSQL + FastAPI
└── README.md
```

---

## 3. System Requirements

- **Python**: 3.10+ (tested on Python 3.14)
- **Node.js**: 18+ or 20+ (tested on v22)
- **Package Managers**: `pip` and `npm`
- **Database**: PostgreSQL 14+ (or built-in SQLite for zero-config local development)
- **Expo Go** or Android Studio / Xcode for running the mobile app

---

## 4. Installation

Clone the repository and inspect the root structure:
```bash
git clone https://github.com/your-org/nutriscan-ai.git
cd nutriscan-ai
```

---

## 5. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install all required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment file:
   ```bash
   cp .env.example .env
   ```

5. Launch the backend server with live reload:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   The backend API will be available at `http://127.0.0.1:8000`.  
   Interactive Swagger documentation is available at `http://127.0.0.1:8000/docs`.

---

## 6. Database Setup & Migrations

NutriScan AI supports both PostgreSQL and SQLite:
- **Default Development**: `sqlite+aiosqlite:///./nutriscan.db` allows immediate, zero-setup execution. Tables are automatically initialized during startup.
- **Production PostgreSQL**: Provide a connection string like:
  ```env
  DATABASE_URL=postgresql+asyncpg://postgres:postgrespassword@localhost:5432/nutriscan
  ```

To run Alembic database migrations:
```bash
# Generate a new migration revision
alembic revision --autogenerate -m "create nutriscan tables"

# Apply migrations
alembic upgrade head
```

Or run via Docker Compose:
```bash
docker compose up -d db
```

---

## 7. Environment Variables

Create `backend/.env` based on `backend/.env.example`:

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | Async SQLAlchemy database URL | `sqlite+aiosqlite:///./nutriscan.db` |
| `JWT_SECRET` | Secret key for signing JWT tokens | Strong 32+ char string |
| `JWT_ALGORITHM` | Cryptographic algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration period | `43200` (30 days) |
| `AI_PROVIDER` | Multimodal provider: `gemini`, `openai`, or `smart_mock` | `gemini` |
| `AI_API_KEY` | API key for Gemini or OpenAI | `""` (activates smart simulator if empty) |
| `AI_MODEL` | Vision model identifier | `gemini-2.0-flash` or `gpt-4o-mini` |
| `CORS_ORIGINS` | Allowed frontend origins | `["*"]` |
| `MAX_UPLOAD_SIZE_MB` | Maximum allowed photo upload size | `10` |

---

## 8. AI Vision API Configuration

NutriScan AI uses an abstracted provider pattern in `app/services/ai_vision_service.py`:

### Google Gemini (Recommended):
1. Obtain an API key from [Google AI Studio](https://aistudio.google.com/).
2. Set in `backend/.env`:
   ```env
   AI_PROVIDER=gemini
   AI_API_KEY=AIzaSy...YourKey...
   AI_MODEL=gemini-2.0-flash
   ```

### OpenAI GPT-4o:
1. Obtain an API key from [OpenAI](https://platform.openai.com/).
2. Set in `backend/.env`:
   ```env
   AI_PROVIDER=openai
   AI_API_KEY=sk-...YourKey...
   AI_MODEL=gpt-4o-mini
   ```

### Zero-Config Offline Fallback:
If `AI_API_KEY` is left blank, the backend automatically activates the built-in **Smart Vision Simulator Engine**. It validates image bytes, verifies format with Pillow, and deterministically generates structured multi-item nutrition data. This ensures testing and demonstrations work without requiring a live cloud credit!

---

## 9. Mobile App Setup

1. Open a new terminal and navigate to `mobile/`:
   ```bash
   cd mobile
   ```

2. Install npm dependencies:
   ```bash
   npm install --legacy-peer-deps
   ```

3. Start the Expo development server:
   ```bash
   npx expo start
   ```

4. Press:
   - `a` to open in Android Emulator
   - `i` to open in iOS Simulator
   - `w` to open in Web Browser
   - Or scan the QR code using the **Expo Go** app on your physical iOS or Android phone!

> **Connecting Physical Phone or Emulator**:
> In the mobile app, navigate to **Profile > App Settings > Backend API Server URL**. Enter your machine's LAN IP (e.g. `http://192.168.1.15:8000/api/v1`) or `http://10.0.2.2:8000/api/v1` for the standard Android emulator.

---

## 10. Android Development

1. Ensure Android Studio is installed with Android SDK Tools and platform 34+.
2. Launch an Android Virtual Device (AVD).
3. Run:
   ```bash
   cd mobile
   npx expo start --android
   ```
   Camera and photo gallery permissions are pre-configured in `mobile/app.json`.

---

## 11. iOS Development

1. Ensure Xcode is installed (macOS required).
2. Open iOS Simulator (`open -a Simulator`).
3. Run:
   ```bash
   cd mobile
   npx expo start --ios
   ```
   Permissions `NSCameraUsageDescription` and `NSPhotoLibraryUsageDescription` are configured in `mobile/app.json`.

---

## 12. API Documentation

Interactive Swagger documentation is available at `http://127.0.0.1:8000/docs`.

### Key Endpoints:

#### Authentication:
- `POST /api/v1/auth/register`: Register user and compute initial targets based on biometrics.
- `POST /api/v1/auth/login`: Authenticate and receive JWT Bearer token.
- `GET /api/v1/auth/me`: Get current authenticated user profile.

#### Food Vision AI & Meals:
- `POST /api/v1/food/analyze`: Multipart/form-data image upload. Analyzes food image, identifies ingredients, estimates grams, and calculates calories & macros.
- `POST /api/v1/meals`: Create and save a meal with detected/customized food items.
- `GET /api/v1/meals/today`: Get all meals logged for today.
- `GET /api/v1/meals?date=YYYY-MM-DD`: Filter meals by specific date.
- `GET /api/v1/meals/{id}`: Get meal details by ID.
- `PUT /api/v1/meals/{id}`: Update meal type, notes, or portion adjustments.
- `DELETE /api/v1/meals/{id}`: Delete a meal.

#### Dashboard & Trends:
- `GET /api/v1/dashboard/today`: Returns consumed vs target calories, remaining macros, water intake, and meals grouped by type.
- `GET /api/v1/dashboard/summary?timeframe=week`: Aggregates historical metrics for charts.

#### Water Tracking:
- `POST /api/v1/water`: Log water intake in ml (e.g. +250ml, +500ml).
- `GET /api/v1/water/today`: Returns today's hydration total, percentage, and log history.
- `DELETE /api/v1/water/{id}`: Delete a water log entry.

#### Profile & Goals:
- `GET /api/v1/profile`: Retrieve user profile anthropometrics and targets.
- `PUT /api/v1/profile`: Update biometrics (age, weight, height, goal) and recalculate targets.
- `PUT /api/v1/profile/goals`: Directly override daily calorie, macro, and water targets.

---

## 13. Running Tests

### Backend Test Suite (Pytest):
Includes 17 automated tests covering authentication, JWT security, food analysis endpoint, meal CRUD, portion mathematics, dashboard metrics, and water tracking:
```bash
cd backend
python -m pytest -v
```
All 17 tests pass with 100% success.

### Frontend Unit Tests (Jest):
Covers proportional weight and serving scaling formulas, meal totals summation, and biometric Mifflin-St Jeor target estimation:
```bash
cd mobile
npx jest
```

### TypeScript Validation:
```bash
cd mobile
npx tsc --noEmit
```

---

## 14. Production Deployment

### Docker Deployment:
To deploy the entire production stack (PostgreSQL + FastAPI Backend) with a single command:
```bash
docker compose up --build -d
```

### Production Checklist:
1. **Security**:
   - Update `JWT_SECRET` in `.env` to a strong random 64-character secret.
   - Configure restrictive `CORS_ORIGINS` to allow only your production mobile domain/scheme.
2. **Reverse Proxy & SSL**:
   - Put Nginx or Caddy in front of the FastAPI app on port 80/443 with Let's Encrypt SSL.
3. **Mobile Binary Build**:
   - Build native `.apk` / `.aab` for Android:
     ```bash
     npx eas-cli build --platform android
     ```
   - Build `.ipa` for iOS TestFlight / App Store:
     ```bash
     npx eas-cli build --platform ios
     ```
