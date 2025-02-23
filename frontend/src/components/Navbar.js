import React, { useMemo } from 'react';
import { AppBar, Toolbar, Typography, Button, Box, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Navbar() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    if (user) {
      logout();
      navigate('/login');
    }
  };

  // Use useMemo to optimize navigation items rendering
  const navItems = useMemo(() => {
    if (user) {
      return (
        <>
          <Button color="inherit" onClick={() => navigate('/courses')}>
            Courses
          </Button>
          <Button color="inherit" onClick={() => navigate('/dashboard')}>
            Dashboard
          </Button>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </>
      );
    } else {
      return (
        <>
          <Button color="inherit" onClick={() => navigate('/login')}>
            Login
          </Button>
          <Button color="inherit" onClick={() => navigate('/register')}>
            Register
          </Button>
        </>
      );
    }
  }, [user, navigate]);

  return (
    <AppBar position="static">
      <Container>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Student Course Registration
          </Typography>
          <Box>{navItems}</Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default Navbar;
