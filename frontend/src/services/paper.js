import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({ baseURL: BASE_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('pp_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const uploadPaper = async (file, onUploadProgress) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/paper/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress,
  });
  return res.data;
};

export const listPapers = async () => {
  const res = await api.get('/paper/list');
  return res.data.papers;
};

export const getPaper = async (paperId) => {
  const res = await api.get(`/paper/${paperId}`);
  return res.data;
};

export const deletePaper = async (paperId) => {
  const res = await api.delete(`/paper/${paperId}`);
  return res.data;
};
