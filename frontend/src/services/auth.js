import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({ baseURL: BASE_URL });

// Attach token from localStorage automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('pp_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ── Auth ──────────────────────────────────────────────────────────────────────

export const signup = (email, password) =>
  api.post('/auth/signup', { email, password });

export const login = async (email, password) => {
  const res = await api.post('/auth/login', { email, password });
  localStorage.setItem('pp_token', res.data.access_token);
  localStorage.setItem('pp_user', JSON.stringify(res.data.user));
  return res.data;
};

export const logout = () => {
  localStorage.removeItem('pp_token');
  localStorage.removeItem('pp_user');
};

export const getStoredUser = () => {
  try {
    return JSON.parse(localStorage.getItem('pp_user'));
  } catch {
    return null;
  }
};

export const isAuthenticated = () => !!localStorage.getItem('pp_token');
