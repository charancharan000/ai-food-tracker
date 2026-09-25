export interface User {
  id: number;
  name: string;
  email: string;
  age?: number | null;
  gender?: string | null;
  height_cm?: number | null;
  weight_kg?: number | null;
  activity_level: string;
  goal: string;
  daily_calorie_target: number;
  protein_target: number;
  carb_target: number;
  fat_target: number;
  daily_water_target_ml: number;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
  age?: number;
  gender?: string;
  height_cm?: number;
  weight_kg?: number;
  activity_level?: string;
  goal?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}
