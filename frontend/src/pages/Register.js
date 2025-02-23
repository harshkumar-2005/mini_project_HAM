import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress
} from '@mui/material';
import api from '../services/api';

function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

function validatePassword(password) {
  return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$/.test(password);
}

function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'student'
  });

  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const validateForm = () => {
    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!validateEmail(formData.email)) newErrors.email = 'Enter a valid email';
    if (!validatePassword(formData.password)) {
      newErrors.password = 'Password must be at least 6 characters, include an uppercase, lowercase & number';
    }
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');
    if (!validateForm()) return;

    setLoading(true);
    try {
      await api.post('/register', {
        name: formData.name,
        email: formData.email,
        password: formData.password,
        role: formData.role
      });
      navigate('/login', { state: { message: 'Registration successful! Please login.' } });
    } catch (err) {
      setApiError(err.response?.data?.error || 'Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: '' }));
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" align="center" gutterBottom>
            Register
          </Typography>

          {apiError && <Alert severity="error" sx={{ mb: 2 }}>{apiError}</Alert>}

          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              fullWidth label="Name" name="name" value={formData.name}
              onChange={handleChange} error={!!errors.name} helperText={errors.name}
              margin="normal" required
            />

            <TextField
              fullWidth label="Email" name="email" type="email" value={formData.email}
              onChange={handleChange} error={!!errors.email} helperText={errors.email}
              margin="normal" required
            />
            
            <TextField
              fullWidth label="Password" name="password" type="password" value={formData.password}
              onChange={handleChange} error={!!errors.password} helperText={errors.password}
              margin="normal" required
            />

            <TextField
              fullWidth label="Confirm Password" name="confirmPassword" type="password"
              value={formData.confirmPassword} onChange={handleChange}
              error={!!errors.confirmPassword} helperText={errors.confirmPassword}
              margin="normal" required
            />

            <FormControl fullWidth margin="normal">
              <InputLabel>Role</InputLabel>
              <Select name="role" value={formData.role} onChange={handleChange} label="Role">
                <MenuItem value="student">Student</MenuItem>
                <MenuItem value="admin">Admin</MenuItem>
              </Select>
            </FormControl>

            <Button
              type="submit" fullWidth variant="contained" size="large"
              sx={{ mt: 3 }} disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Register'}
            </Button>

            <Button fullWidth variant="text" onClick={() => navigate('/login')} sx={{ mt: 1 }}>
              Already have an account? Login
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default Register;
