import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({ baseURL: BASE_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('pp_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const getChatHistory = async (paperId) => {
  const res = await api.get(`/paper/${paperId}/chat`);
  return res.data.history;
};

export const sendChatMessage = async (paperId, question) => {
  const res = await api.post(`/paper/${paperId}/chat`, { question });
  return res.data;
};
