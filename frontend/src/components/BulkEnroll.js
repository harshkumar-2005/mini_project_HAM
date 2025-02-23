import { useState } from 'react';
import {
  Box,
  Checkbox,
  FormControlLabel,
  Button,
  Typography,
  Paper,
  List,
  ListItem,
  Snackbar,
  Alert,
  CircularProgress
} from '@mui/material';
import { bulkEnroll } from '../services/api';

function BulkEnroll({ courses, onEnrollmentComplete }) {
  const [selectedCourses, setSelectedCourses] = useState([]);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [loading, setLoading] = useState(false);

  const handleToggleCourse = (courseId) => {
    setSelectedCourses((prev) =>
      prev.includes(courseId)
        ? prev.filter((id) => id !== courseId)
        : [...prev, courseId]
    );
  };

  const handleBulkEnroll = async () => {
    setLoading(true);
    try {
      const result = await bulkEnroll(selectedCourses);
      setSnackbar({
        open: true,
        message: `Successfully enrolled in ${result.enrolled.length} courses`,
        severity: 'success',
      });
      setSelectedCourses([]);
      if (onEnrollmentComplete) onEnrollmentComplete();
    } catch (err) {
      setSnackbar({
        open: true,
        message: err.response?.data?.message || 'Failed to enroll in courses',
        severity: 'error',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Bulk Enrollment
      </Typography>
      <List>
        {courses.map((course) => (
          <ListItem key={course.id}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={selectedCourses.includes(course.id)}
                  onChange={() => handleToggleCourse(course.id)}
                  disabled={loading} // Prevent changes while processing
                />
              }
              label={course.name}
            />
          </ListItem>
        ))}
      </List>
      <Box sx={{ mt: 2 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleBulkEnroll}
          disabled={selectedCourses.length === 0 || loading}
        >
          {loading ? <CircularProgress size={24} /> : 'Enroll in Selected Courses'}
        </Button>
      </Box>
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity}>{snackbar.message}</Alert>
      </Snackbar>
    </Paper>
  );
}

export default BulkEnroll;
