import { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  Divider,
  CircularProgress,
  Alert,
  Button
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import CourseList from '../components/CourseList';
import BulkEnroll from '../components/BulkEnroll';
import { useFetch } from '../hooks/useFetch';

function StudentDashboard() {
  const { user } = useAuth();
  const { data: enrollments, loading, error, refetch } = useFetch('/enrollments');
  const { data: courses, loading: coursesLoading } = useFetch('/courses'); // Fetch available courses

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Welcome Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h4" gutterBottom>
              Welcome, {user.name}!
            </Typography>
            <Typography color="textSecondary">Student Dashboard</Typography>
          </Paper>
        </Grid>

        {/* Enrolled Courses */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              My Enrolled Courses
            </Typography>
            <Divider sx={{ mb: 2 }} />

            {loading ? (
              <Box display="flex" justifyContent="center" alignItems="center">
                <CircularProgress />
              </Box>
            ) : error ? (
              <Alert severity="error">{error}</Alert>
            ) : enrollments?.length > 0 ? (
              <Grid container spacing={2}>
                {enrollments.map((enrollment) => (
                  <Grid item xs={12} md={4} key={enrollment.id}>
                    <Card>
                      <CardContent>
                        <Typography variant="h6">{enrollment.course.name}</Typography>
                        <Typography color="textSecondary">{enrollment.course.description}</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            ) : (
              <Box textAlign="center">
                <Typography color="textSecondary">You are not enrolled in any courses yet.</Typography>
                <Button
                  variant="contained"
                  color="primary"
                  sx={{ mt: 2 }}
                  onClick={refetch}
                >
                  Browse Courses
                </Button>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Available Courses */}
        <Grid item xs={12}>
          {coursesLoading ? (
            <Box display="flex" justifyContent="center" alignItems="center">
              <CircularProgress />
            </Box>
          ) : (
            <CourseList courses={courses} onEnrollmentComplete={refetch} />
          )}
        </Grid>

        {/* Bulk Enrollment */}
        <Grid item xs={12}>
          {coursesLoading ? (
            <Box display="flex" justifyContent="center" alignItems="center">
              <CircularProgress />
            </Box>
          ) : (
            <BulkEnroll courses={courses} onEnrollmentComplete={refetch} />
          )}
        </Grid>
      </Grid>
    </Container>
  );
}

export default StudentDashboard;
