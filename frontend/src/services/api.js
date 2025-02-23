import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle unauthorized requests (401)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login'; // Redirect to login page
    }
    return Promise.reject(error);
  }
);

// Utility function to handle API calls
const handleRequest = async (request) => {
  try {
    const response = await request;
    return response.data;
  } catch (error) {
    console.error('API Error:', error.response?.data || error.message);
    throw error.response?.data || { message: 'Something went wrong!' };
  }
};

export const loginUser = (email, password) =>
  handleRequest(api.post('/login', { email, password }));

export const getCourses = () => handleRequest(api.get('/courses'));

export const enrollCourse = (courseId) =>
  handleRequest(api.post('/enroll', { course_id: courseId }));

export const bulkEnroll = (courseIds) =>
  handleRequest(api.post('/bulk-enroll', { course_ids: courseIds }));

export default api;
