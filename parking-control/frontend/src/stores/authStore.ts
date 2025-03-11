import create from 'zustand';
import axios from 'axios';

interface AuthState {
  token: string | null;
  user: {
    id: number;
    email: string;
    apartment: string;
  } | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  googleLogin: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('token'),
  user: JSON.parse(localStorage.getItem('user') || 'null'),
  isAuthenticated: !!localStorage.getItem('token'),
  
  login: async (email: string, password: string) => {
    try {
      const response = await axios.post('/api/auth/token', {
        username: email,
        password,
      });
      
      const { access_token, user } = response.data;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      
      set({
        token: access_token,
        user,
        isAuthenticated: true,
      });
    } catch (error) {
      throw new Error('Falha na autenticação');
    }
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    set({
      token: null,
      user: null,
      isAuthenticated: false,
    });
  },
  
  googleLogin: async () => {
    // TODO: Implementar login com Google via Cognito
    throw new Error('Login com Google ainda não implementado');
  },
})); 