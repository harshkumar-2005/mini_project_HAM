import { useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  Alert,
  CircularProgress,
  Box
} from '@mui/material';
import { useFetch } from '../hooks/useFetch';
import api from '../services/api';

function AdminDashboard() {
  const [newCourse, setNewCourse] = useState({ name: '', description: '', prerequisite_id: '' });
  const [dialogOpen, setDialogOpen] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
  const [deletingCourseId, setDeletingCourseId] = useState(null);

  const { data: courses, loading, error, refetch } = useFetch('/courses');
  const { data: students } = useFetch('/students');

  const handleAddCourse = async () => {
    if (!newCourse.name.trim() || !newCourse.description.trim()) {
      setSnackbar({ open: true, message: 'All fields are required', severity: 'error' });
      return;
    }
    try {
      await api.post('/courses', newCourse);
      setDialogOpen(false);
      setNewCourse({ name: '', description: '', prerequisite_id: '' });
      refetch();
      setSnackbar({ open: true, message: 'Course added successfully', severity: 'success' });
    } catch (err) {
      setSnackbar({ open: true, message: err.response?.data?.error || 'Failed to add course', severity: 'error' });
    }
  };

  const handleDeleteCourse = async (id) => {
    if (!window.confirm('Are you sure you want to delete this course?')) return;
    setDeletingCourseId(id);
    try {
      await api.delete(`/courses/${id}`);
      refetch();
      setSnackbar({ open: true, message: 'Course deleted successfully', severity: 'success' });
    } catch (err) {
      setSnackbar({ open: true, message: err.response?.data?.error || 'Failed to delete course', severity: 'error' });
    } finally {
      setDeletingCourseId(null);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Statistics Overview */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Total Courses</Typography>
            <Typography variant="h4">{loading ? <CircularProgress size={24} /> : courses?.length || 0}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6">Total Students</Typography>
            <Typography variant="h4">{students?.length || 0}</Typography>
          </Paper>
        </Grid>

        {/* Course Management */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
              <Typography variant="h6">Course Management</Typography>
              <Button variant="contained" onClick={() => setDialogOpen(true)}>Add New Course</Button>
            </Box>

            {loading ? (
              <Box display="flex" justifyContent="center" alignItems="center">
                <CircularProgress />
              </Box>
            ) : error ? (
              <Alert severity="error">{error}</Alert>
            ) : (
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Name</TableCell>
                    <TableCell>Description</TableCell>
                    <TableCell>Prerequisite</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {courses?.map((course) => (
                    <TableRow key={course.id}>
                      <TableCell>{course.name}</TableCell>
                      <TableCell>{course.description}</TableCell>
                      <TableCell>{course.prerequisite?.name || 'None'}</TableCell>
                      <TableCell>
                        <Button color="primary">Edit</Button>
                        <Button 
                          color="error" 
                          onClick={() => handleDeleteCourse(course.id)}
                          disabled={deletingCourseId === course.id}
                        >
                          {deletingCourseId === course.id ? <CircularProgress size={20} /> : 'Delete'}
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Add Course Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
        <DialogTitle>Add New Course</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Course Name"
            value={newCourse.name}
            onChange={(e) => setNewCourse({ ...newCourse, name: e.target.value })}
            margin="normal"
          />
          <TextField
            fullWidth
            label="Description"
            value={newCourse.description}
            onChange={(e) => setNewCourse({ ...newCourse, description: e.target.value })}
            margin="normal"
            multiline
            rows={3}
          />
          <TextField
            fullWidth
            select
            label="Prerequisite"
            value={newCourse.prerequisite_id}
            onChange={(e) => setNewCourse({ ...newCourse, prerequisite_id: e.target.value })}
            margin="normal"
            SelectProps={{ native: true }}
          >
            <option value="">None</option>
            {courses?.map((course) => (
              <option key={course.id} value={course.id}>{course.name}</option>
            ))}
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleAddCourse} 
            variant="contained"
            disabled={!newCourse.name.trim() || !newCourse.description.trim()}
          >
            Add Course
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar open={snackbar.open} autoHideDuration={6000} onClose={() => setSnackbar({ ...snackbar, open: false })}>
        <Alert severity={snackbar.severity}>{snackbar.message}</Alert>
      </Snackbar>
    </Container>
  );
}

export default AdminDashboard;
