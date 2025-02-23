import { Box, Typography, Button, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Home() {
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          mt: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontSize: { xs: '2rem', md: '3rem' } }}>
          Student Course Registration System
        </Typography>
        <Typography variant="h5" color="textSecondary" paragraph>
          Manage your course enrollments efficiently and easily
        </Typography>
        
        {!user ? (
          <Box sx={{ mt: 4 }}>
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={() => navigate('/login')}
              sx={{ mr: 2, px: 4 }}
            >
              Login
            </Button>
          </Box>
        ) : (
          <Box sx={{ mt: 4 }}>
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={() => navigate(user.role === 'admin' ? '/admin' : '/dashboard')}
              sx={{ px: 4 }}
            >
              Go to Dashboard
            </Button>
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default Home;
