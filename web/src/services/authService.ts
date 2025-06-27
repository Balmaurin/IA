import api from './apiClient';
export const login = (data:any) => api.post('/api/auth/login', data);
export const register = (data:any) => api.post('/api/auth/register', data);
