import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface User {
  id: string;
  username: string;
  email: string;
}

interface Credentials {
  username: string;
  password: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Create axios instance with base URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8001',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor to handle 401 Unauthorized responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth data on 401 Unauthorized
      localStorage.removeItem('access_token');
      localStorage.removeItem('username');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  // Set up request interceptor to add auth token
  useEffect(() => {
    const requestInterceptor = api.interceptors.request.use((config) => {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    return () => {
      api.interceptors.request.eject(requestInterceptor);
    };
  }, []);

  // Check if user is already logged in on initial load
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchUserData(token).catch(() => {
        // If token is invalid, clear it
        localStorage.removeItem('access_token');
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUserData = async (token: string) => {
    try {
      // Get username from token or localStorage
      const username = localStorage.getItem('username');
      if (!username) {
        throw new Error('No username found');
      }
      
      // Set basic user data
      setUser({
        id: 'user-id', // This would come from the API in a real implementation
        username,
        email: '',
      });
    } catch (err) {
      console.error('Failed to fetch user data', err);
      localStorage.removeItem('access_token');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const login = async (username: string, password: string) => {
    try {
      setError(null);
      setLoading(true);
      
      const response = await api.post<AuthResponse>('/api/auth/login', {
        username,
        password,
      });
      
      const { access_token } = response.data;
      
      localStorage.setItem('access_token', access_token);
      localStorage.setItem('username', username);
      
      await fetchUserData(access_token);
      navigate('/dashboard');
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Login failed';
      setError(Array.isArray(errorMessage) ? errorMessage[0] : errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (username: string, password: string) => {
    try {
      setError(null);
      setLoading(true);
      
      await api.post('/api/auth/register', {
        username,
        password,
      });
      
      // After successful registration, log the user in
      await login(username, password);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Registration failed';
      setError(Array.isArray(errorMessage) ? errorMessage[0] : errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await api.post('/api/auth/logout');
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('username');
      setUser(null);
      navigate('/login');
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

// Export the useAuth hook
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Export the configured axios instance for use in other components
export { api };
