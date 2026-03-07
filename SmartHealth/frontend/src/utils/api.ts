import axios from 'axios';
import { useAuthStore } from '../stores/authStore';

const API_BASE_URL = import.meta.env.PUBLIC_API_BASE_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;

export const authAPI = {
  register: (data: { email: string; password: string; username: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getCurrentUser: () => api.get('/auth/me'),
  updateProfile: (data: any) => api.put('/auth/me', data),
  refreshToken: () => api.post('/auth/refresh'),
};

export const healthAPI = {
  getIndicators: () => api.get('/health/indicators'),
  createIndicator: (data: any) => api.post('/health/indicators', data),
  getRecords: (params?: any) => api.get('/health/records', { params }),
  createRecord: (data: any) => api.post('/health/records', data),
  getStats: () => api.get('/health/stats'),
};

export const dietAPI = {
  getFoods: (params?: any) => api.get('/diet/foods', { params }),
  getFoodTypes: () => api.get('/diet/food-types'),
  getRecords: (params?: any) => api.get('/diet/records', { params }),
  createRecord: (data: any) => api.post('/diet/records', data),
  getDailyStats: (date?: string) => api.get('/diet/stats/daily', { params: { date } }),
};

export const exerciseAPI = {
  getExercises: (params?: any) => api.get('/exercise/exercises', { params }),
  getExerciseTypes: () => api.get('/exercise/exercise-types'),
  getRecords: (params?: any) => api.get('/exercise/records', { params }),
  createRecord: (data: any) => api.post('/exercise/records', data),
  getDailyStats: (date?: string) => api.get('/exercise/stats/daily', { params: { date } }),
};

export const articleAPI = {
  getArticles: (params?: any) => api.get('/article/articles', { params }),
  getArticle: (id: string) => api.get(`/article/articles/${id}`),
  createArticle: (data: any) => api.post('/article/articles', data),
  getTypes: () => api.get('/article/types'),
};

export const aiAPI = {
  analyze: (days: number = 7) => api.post('/ai/analyze', { days }),
  getReports: (params?: any) => api.get('/ai/reports', { params }),
  getReport: (id: string) => api.get(`/ai/reports/${id}`),
};
