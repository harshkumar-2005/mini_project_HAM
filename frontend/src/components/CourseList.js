import { useState } from 'react';
import { Card, CardContent, CardActions, Button, Typography, Grid, CircularProgress, Alert } from '@mui/material';
import { useFetch } from '../hooks/useFetch';
import { enrollCourse } from '../services/api';

function CourseList() {
  const { data: courses, loading, error } = useFetch('/courses');
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  const handleEnroll = async (courseId) => {
    try {
      await enrollCourse(courseId);
      setEnrolledCourses([...enrolledCourses, courseId]);
    } catch (err) {
      console.error('Enrollment failed:', err);
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Grid container spacing={3}>
      {courses && courses.length > 0 ? (
        courses.map((course) => (
          <Grid item xs={12} sm={6} md={4} key={course.id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{course.name}</Typography>
                <Typography variant="body2" color="textSecondary">
                  {course.description}
                </Typography>
              </CardContent>
              <CardActions>
                <Button 
                  variant="contained" 
                  color="primary" 
                  onClick={() => handleEnroll(course.id)}
                  disabled={enrolledCourses.includes(course.id)}
                >
                  {enrolledCourses.includes(course.id) ? 'Enrolled' : 'Enroll'}
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))
      ) : (
        <Typography variant="body1">No courses available.</Typography>
      )}
    </Grid>
  );
}

export default CourseList;
