import api from './apiClient';
export const getBalance = (user:string) => api.get(`/api/tokens?user=${user}`);
