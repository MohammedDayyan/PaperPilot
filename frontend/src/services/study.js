import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({ baseURL: BASE_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('pp_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ── Quiz ──────────────────────────────────────────────────────────────────────
export const getQuiz = async (paperId) => {
  const res = await api.get(`/paper/${paperId}/quiz`);
  return res.data.quiz;
};

export const generateQuiz = async (paperId) => {
  const res = await api.post(`/paper/${paperId}/quiz`);
  return res.data.quiz;
};

// ── Flashcards ────────────────────────────────────────────────────────────────
export const getFlashcards = async (paperId) => {
  const res = await api.get(`/paper/${paperId}/flashcards`);
  return res.data.cards;
};

export const generateFlashcards = async (paperId) => {
  const res = await api.post(`/paper/${paperId}/flashcards`);
  return res.data.cards;
};

// ── Study Advice ──────────────────────────────────────────────────────────────
export const getAdvice = async (paperId) => {
  const res = await api.get(`/paper/${paperId}/advice`);
  return res.data.advice;
};

export const generateAdvice = async (paperId) => {
  const res = await api.post(`/paper/${paperId}/advice`);
  return res.data.advice;
};

// ── Delete Endpoints ──────────────────────────────────────────────────────────
export const deleteQuiz = async (paperId) => {
  const res = await api.delete(`/paper/${paperId}/quiz`);
  return res.data;
};

export const deleteFlashcards = async (paperId) => {
  const res = await api.delete(`/paper/${paperId}/flashcards`);
  return res.data;
};

export const deleteAdvice = async (paperId) => {
  const res = await api.delete(`/paper/${paperId}/advice`);
  return res.data;
};
