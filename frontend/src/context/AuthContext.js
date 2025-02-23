import { createContext, useState, useContext, useEffect } from 'react';
// import api from '../api'; // Import API to verify token
import api from '../services/api';


const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const verifyUser = async () => {
      try {
        const savedUser = localStorage.getItem('user');
        const token = localStorage.getItem('token');

        if (savedUser && token) {
          const parsedUser = JSON.parse(savedUser);

          // Verify token with backend
          await api.get('/verify-token'); // API should return 200 if valid

          setUser(parsedUser);
        } else {
          logout(); // Clear invalid session
        }
      } catch (error) {
        console.error('Token verification failed:', error);
        logout(); // Auto logout on failure
      } finally {
        setLoading(false);
      }
    };

    verifyUser();
  }, []);

  const login = (userData, token) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', token);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    window.location.href = '/login'; // Redirect to login page
  };

  if (loading) {
    return <div>Loading...</div>; // Add a better loading UI
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
